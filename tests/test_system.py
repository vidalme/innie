"""Testes sem rede e sem modelo: python3 -m unittest discover -s tests -v."""
import copy
from types import SimpleNamespace
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pdi_copilot.model import PDIError, apply_operations, cycle, validate, window
from pdi_copilot.storage import Store, digest, read_json, write_json
from pdi_copilot.operations import (apply_proposal, backup, close_cycle, connect, create_cycle, doctor,
                                   git_check, import_source, init_git, prepare_proposal, restore, start_cycle, verify_archive)
from pdi_copilot.views import export_pdi, overview, render
from pdi_copilot.cli import carry, adendum, parser, run

class SystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.innie = self.base / "innie"; self.innie.mkdir()
        (self.innie / ".gitignore").write_text('/pessoal\n/.local/\n')
        self.store = Store(self.base / "outtie"); self.store.initialize()

    def tearDown(self): self.tmp.cleanup()

    def new_cycle(self, cid="cycle-1"):
        create_cycle(self.store, cid, "Ciclo fictício", "2026-07-01", "2027-05-31", "2027-04-30", "2027-05-15")
        start_cycle(self.store, cid, True)

    def change(self, operations):
        p = prepare_proposal(self.store, operations, "Teste revisado")
        return apply_proposal(self.store, p["proposal"], True)

    def action(self, **fields):
        self.change([{"op":"upsert", "collection":"actions", "value":{"id":"a1", "title":"Atividade fictícia", "status":"planned", "due_on":"2027-03-01", "effort_hours":2, **fields}}])

    def test_setup_idempotent(self):
        self.assertFalse(self.store.initialize()); self.assertEqual(self.store.load()["revision"], 0)

    def test_existing_unknown_folder_is_preserved(self):
        target = self.base / 'old'; target.mkdir(); (target/'secret.txt').write_text('preserve')
        with self.assertRaises(PDIError): Store(target).initialize()
        self.assertEqual((target/'secret.txt').read_text(), 'preserve')

    def test_link_and_doctor(self):
        connect(self.innie, self.store.root)
        self.assertTrue(doctor(self.innie, self.store)['ok'])

    def test_setup_workspace_resolves_both_roots_on_repeat(self):
        before = self.store.load()
        with patch('pdi_copilot.cli.INNIE', self.innie):
            for _ in range(2):
                result = run(parser().parse_args(['--outtie', str(self.store.root), 'setup']))
                workspace = Path(result['workspace'])
                roots = [(workspace.parent / f['path']).resolve()
                         for f in read_json(workspace)['folders']]
                self.assertEqual(roots, [self.innie, self.store.root])
        self.assertEqual(self.store.load(), before)

    def test_setup_rejects_nested_destination_before_creating_state(self):
        target = self.innie / 'private-state'
        with patch('pdi_copilot.cli.INNIE', self.innie):
            with self.assertRaises(PDIError):
                run(parser().parse_args(['--outtie', str(target), 'setup']))
        self.assertFalse(target.exists())

    def test_setup_rejects_conflicting_link_before_creating_state(self):
        connect(self.innie, self.store.root)
        target = self.base / 'new-private-state'
        with patch('pdi_copilot.cli.INNIE', self.innie):
            with self.assertRaises(PDIError):
                run(parser().parse_args(['--outtie', str(target), 'setup']))
        self.assertFalse(target.exists())
        self.assertEqual((self.innie / 'pessoal').resolve(), self.store.root)

    def test_connect_workspace_follows_custom_destination(self):
        connect(self.innie, self.store.root)
        target = Store(self.base / 'outro espaço'); target.initialize()
        with patch('pdi_copilot.cli.INNIE', self.innie):
            result = run(parser().parse_args(['--outtie', str(target.root), 'connect', '--switch']))
        workspace = Path(result['workspace'])
        folders = read_json(workspace)['folders']
        self.assertEqual((workspace.parent / folders[1]['path']).resolve(), target.root)
        self.assertEqual((self.innie / 'pessoal').resolve(), target.root)
        self.assertTrue(self.store.root.exists())

    def test_workspace_single_root_opt_out_and_legacy_flag(self):
        with patch('pdi_copilot.cli.INNIE', self.innie):
            for command in ('setup', 'connect'):
                for flag, count in [('--no-two-roots', 1), ('--two-roots', 2)]:
                    result = run(parser().parse_args(['--outtie', str(self.store.root), command, flag]))
                    self.assertEqual(len(read_json(result['workspace'])['folders']), count)

    def test_bootstrap_without_arguments_and_explicit_command(self):
        source = Path(__file__).resolve().parents[1]
        shutil.copytree(source / 'scripts', self.innie / 'scripts')
        shutil.copytree(source / 'src', self.innie / 'src')
        shutil.copyfile(source / 'pdi.code-workspace', self.innie / 'pdi.code-workspace')
        before = self.store.load()
        for _ in range(2):
            result = subprocess.run(['bash', str(self.innie / 'scripts/bootstrap.sh')],
                                    cwd=self.base, check=True, capture_output=True, text=True)
            workspace = Path(json.loads(result.stdout)['workspace'])
            self.assertEqual([(workspace.parent / f['path']).resolve()
                              for f in read_json(workspace)['folders']], [self.innie, self.store.root])
        shared = read_json(self.innie / 'pdi.code-workspace')
        self.assertEqual([(self.innie / f['path']).resolve() for f in shared['folders']],
                         [self.innie, self.store.root])
        result = subprocess.run(['bash', str(self.innie / 'scripts/bootstrap.sh'), 'state'],
                                cwd=self.base, check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), before)

    def test_connect_does_not_replace_real_folder(self):
        (self.innie/'pessoal').mkdir()
        with self.assertRaises(PDIError): connect(self.innie, self.store.root)

    def test_connect_rejects_nested_root(self):
        target=Store(self.innie/'nested');target.initialize()
        with self.assertRaises(PDIError):connect(self.innie,target.root)

    def test_git_ignore_and_no_private_tracking(self):
        init_git(self.innie)
        connect(self.innie,self.store.root)
        self.assertEqual(git_check(self.innie)['status'],'ok')
        subprocess.run(['git','-C',str(self.innie),'add','-f','pessoal'],check=True,capture_output=True)
        self.assertEqual(git_check(self.innie)['status'],'error')
        with self.assertRaises(PDIError):connect(self.innie,self.store.root)

    def test_cycle_requires_calendar_for_start(self):
        create_cycle(self.store,'empty','Sem datas')
        with self.assertRaises(PDIError):start_cycle(self.store,'empty',True)

    def test_single_active_cycle(self):
        self.new_cycle();create_cycle(self.store,'cycle-2','Segundo','2027-06-01','2028-03-31','2028-02-29')
        with self.assertRaises(PDIError):start_cycle(self.store,'cycle-2',True)

    def test_proposal_approval_required(self):
        self.new_cycle();p=prepare_proposal(self.store,[{'op':'profile','value':{'seniority':'Júnior'}}],'Revisão')
        with self.assertRaises(PDIError):apply_proposal(self.store,p['proposal'])

    def test_revision_conflict(self):
        self.new_cycle();ops=[{'op':'profile','value':{'seniority':'Júnior'}}]
        p1=prepare_proposal(self.store,ops,'Primeira');p2=prepare_proposal(self.store,ops,'Segunda')
        apply_proposal(self.store,p1['proposal'],True)
        with self.assertRaises(PDIError):apply_proposal(self.store,p2['proposal'],True)

    def test_failed_publication_preserves_state(self):
        self.new_cycle();before=self.store.load()
        original=write_json
        def fail_head(path,obj):
            if Path(path).name=='metadata.json':raise OSError('simulated failure')
            return original(path,obj)
        with self.store.lock(),patch('pdi_copilot.storage.write_json',side_effect=fail_head):
            with self.assertRaises(OSError):self.store.commit(copy.deepcopy(before),before['revision'],'Failure')
        self.assertEqual(self.store.load(),before)
        self.change([{'op':'profile','value':{'seniority':'Júnior'}}])
        self.assertEqual(self.store.load()['revision'],before['revision']+1)

    def test_tamper_hash_detected(self):
        path=self.store.root/'revisions/00000000.json';path.write_text('{}')
        with self.assertRaises(PDIError):self.store.load()

    def test_source_import_deduplicates(self):
        f=self.base/'input.md';f.write_text('# Evidência fictícia')
        first=import_source(self.store,f);second=import_source(self.store,f)
        self.assertEqual(first['id'],second['id']);self.assertFalse(second['imported'])

    def test_html_skips_scripts(self):
        f=self.base/'input.html';f.write_text('<script>do not run</script><p>Visível</p>')
        row=import_source(self.store,f)
        self.assertEqual((self.store.root/row['extracted_path']).read_text().strip(),'Visível')

    def test_image_requires_review(self):
        f=self.base/'input.png';f.write_bytes(b'fixture-not-real-image')
        row=import_source(self.store,f);self.assertIsNone(row['extracted_path'])

    def test_future_due_can_be_done(self):
        self.new_cycle();self.action(status='done',completed_on='2026-10-01')
        self.assertEqual(cycle(self.store.load())['actions'][0]['status'],'done')

    def test_cycle_dependency_rejected(self):
        self.new_cycle()
        with self.assertRaises(PDIError):self.action(depends_on=['a1'])

    def test_dependency_loop_rejected(self):
        self.new_cycle()
        ops=[{'op':'upsert','collection':'actions','value':{'id':a,'title':a,'status':'planned','depends_on':[b]}} for a,b in [('a','b'),('b','a')]]
        with self.assertRaises(PDIError):self.change(ops)

    def test_missing_evidence_reference_rejected(self):
        self.new_cycle()
        with self.assertRaises(PDIError):self.action(evidence_ids=['missing'])

    def test_official_confirmation_needs_source(self):
        self.new_cycle()
        with self.assertRaises(PDIError):self.change([{'op':'upsert','collection':'criterion_assessments','value':{'id':'c1','criterion_id':'CI-05','status':'confirmed'}}])

    def test_assessment_type_required(self):
        self.new_cycle()
        with self.assertRaises(PDIError):self.change([{'op':'upsert','collection':'competency_assessments','value':{'id':'hs1'}}])

    def test_calendar_month_boundary(self):
        r=window('2026-10-31','2027-04-30',6)
        self.assertEqual(r['lower_bound'],'2026-10-30');self.assertEqual(r['status'],'within_window')

    def test_boundary_pending(self):
        self.assertEqual(window('2026-10-30','2027-04-30',6)['status'],'boundary_pending')

    def test_outside_window(self):
        self.assertEqual(window('2025-10-01','2027-04-30',12)['status'],'outside_window')

    def test_status_does_not_claim_official_compliance(self):
        self.new_cycle();self.action(status='cancelled')
        status=overview(self.store.load(),on='2027-04-01')
        self.assertEqual(status['changed_commitments'],['a1']);self.assertEqual(status['official_pdi_compliance'],'not_determined')

    def test_manual_render_edits_preserved(self):
        self.new_cycle();self.action();render(self.store)
        view=self.store.root/'cycles/cycle-1/outputs/plano.md';view.write_text('Minha edição')
        with self.assertRaises(PDIError):render(self.store)
        render(self.store,preserve_edits=True)
        self.assertTrue(any(p.read_text()=='Minha edição' for p in (self.store.root/'inbox').glob('*')))

    def test_export_limits_utf16(self):
        self.new_cycle();self.action(pdi_description='😀'*8001)
        with self.assertRaises(PDIError):export_pdi(self.store,'a1')

    def test_export_does_not_register_external(self):
        self.new_cycle();self.action(description='Planejamento fictício')
        self.assertEqual(export_pdi(self.store,'a1')['external_registration'],'not_confirmed')

    def test_archive_and_next_cycle(self):
        self.new_cycle();self.action();render(self.store)
        r=close_cycle(self.store,'cycle-1',self.innie,True)
        self.assertTrue(verify_archive(self.store.root/r['archive'])['verified'])
        self.assertIsNone(self.store.load()['active_cycle'])
        self.assertFalse(close_cycle(self.store,'cycle-1',self.innie,True)['closed'])
        with self.assertRaises(PDIError):render(self.store,'cycle-1')
        create_cycle(self.store,'cycle-2','Novo','2027-06-01','2028-03-31','2028-03-01');start_cycle(self.store,'cycle-2',True)
        self.assertEqual(cycle(self.store.load())['criterion_assessments'],[])

    def test_archive_change_is_blocked(self):
        self.new_cycle();close_cycle(self.store,'cycle-1',self.innie,True)
        with self.assertRaises(PDIError):self.change([{'op':'calendar','cycle_id':'cycle-1','value':{'label':'changed'}}])

    def test_archive_tamper_detected(self):
        self.new_cycle();r=close_cycle(self.store,'cycle-1',self.innie,True)
        path=self.store.root/r['archive'];(path/'cycle.json').write_text('{}')
        with self.assertRaises(PDIError):verify_archive(path)

    def test_backup_restore(self):
        self.new_cycle();self.action();render(self.store)
        b=self.base/'backup.zip';backup(self.store,b)
        target=self.base/'restored';restore(b,target)
        self.assertEqual(Store(target).load(),self.store.load())
        connect(self.innie,target,switch=True);self.assertTrue(doctor(self.innie,Store(target))['ok'])

    def test_restore_rejects_overwrite(self):
        b=self.base/'backup.zip';backup(self.store,b)
        with self.assertRaises(PDIError):restore(b,self.store.root)

    def test_zip_traversal_rejected(self):
        b=self.base/'bad.zip'
        with zipfile.ZipFile(b,'w') as z:z.writestr('../escape','bad')
        with self.assertRaises(PDIError):restore(b,self.base/'restore')
        self.assertFalse((self.base/'escape').exists())

    def test_invalid_id_rejected(self):
        with self.assertRaises(PDIError):create_cycle(self.store,'../bad','Bad')

    def test_delete_operation_rejected(self):
        with self.assertRaises(PDIError):self.change([{'op':'delete','collection':'sources','id':'a'}])

    def test_restored_views_keep_provenance(self):
        self.new_cycle(); self.action(); render(self.store)
        archive=self.base/'backup.zip'; backup(self.store,archive)
        restored=self.base/'restored'; restore(archive,restored)
        self.assertTrue((restored/'.runtime/views.json').is_file())
        render(Store(restored))
        close_cycle(Store(restored),'cycle-1',self.innie,True)

    def test_metric_source_preserved_in_archive(self):
        self.new_cycle()
        original=self.base/'metric.txt'; original.write_text('medição fictícia')
        imported=import_source(self.store,original,'personal','Métrica')
        source_id=imported['id']
        self.change([{'op':'upsert','collection':'metrics','value':{'id':'m1','name':'Métrica','value':1,'source_ids':[source_id]}}])
        result=close_cycle(self.store,'cycle-1',self.innie,True)
        folder=self.store.root/result['archive']
        rows=read_json(folder/'sources.json')
        self.assertEqual(rows[0]['id'],source_id)
        self.assertTrue((folder/rows[0]['local_path']).exists())
        verify_archive(folder)

    def test_export_accepts_null_description(self):
        self.new_cycle(); self.action(description=None)
        export_pdi(self.store,'a1')

    def test_nested_dates_and_references(self):
        self.new_cycle()
        invalid=[('metrics',{'id':'m1','source_ids':['missing']}),
                 ('metrics',{'id':'m1','period_start':'2026-99-99'}),
                 ('metrics',{'id':'m1','baseline':-100}),
                 ('metrics',{'id':'m1','period_start':'2027-03-01','period_end':'2027-02-01'}),
                 ('events',{'id':'e1','occurred_on':'tomorrow'}),
                 ('events',{'id':'e1','related_action_ids':['missing']}),
                 ('competency_assessments',{'id':'c1','assessment_type':'self','assessed_on':'yesterday'})]
        for collection,value in invalid:
            with self.subTest(value=value), self.assertRaises(PDIError):
                self.change([{'op':'upsert','collection':collection,'value':value}])

    def test_unknown_schema_unchanged(self):
        meta=self.store.root/'metadata.json';old=read_json(meta);old['schema_version']=99;write_json(meta,old)
        before=meta.read_bytes()
        with self.assertRaises(PDIError):self.store.initialize()
        self.assertEqual(meta.read_bytes(),before)

    def test_carry_preserves_old_and_clears_external_registration(self):
        self.new_cycle(); self.action(external_id='old', external_registration='confirmed')
        close_cycle(self.store,'cycle-1',self.innie,True)
        create_cycle(self.store,'next','Próximo','2027-06-01','2028-03-31','2028-03-01')
        args=SimpleNamespace(approve=True,from_cycle='cycle-1',to_cycle='next',action='a1',due='2027-08-01')
        self.assertTrue(carry(self.store,args)['carried'])
        self.assertFalse(carry(self.store,args)['carried'])
        state=self.store.load(); old=cycle(state,'cycle-1')['actions'][0]; new=cycle(state,'next')['actions'][0]
        self.assertEqual(old['external_id'],'old'); self.assertNotIn('external_id',new)
        self.assertEqual(new['evidence_ids'],[])

    def test_adendum_does_not_change_frozen_archive(self):
        self.new_cycle(); result=close_cycle(self.store,'cycle-1',self.innie,True)
        frozen=self.store.root/result['archive']; before=digest(frozen/'cycle.json')
        source=self.base/'late.txt'; source.write_text('resultado posterior fictício')
        adendum(self.store,SimpleNamespace(approve=True,id='cycle-1',file=str(source),reason='Documento recebido depois'))
        self.assertEqual(before,digest(frozen/'cycle.json')); verify_archive(frozen)
        self.assertEqual(len(cycle(self.store.load(),'cycle-1')['adenda']),1)

    def test_malformed_operation_rejected(self):
        with self.assertRaises(PDIError): self.change(['not-an-object'])

if __name__=='__main__': unittest.main()
