"""Testes sem rede e sem modelo: python3 -m unittest discover -s tests -v."""
import copy
from types import SimpleNamespace
import json
import os
import shlex
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

    def test_guidance_before_setup_does_not_create_space(self):
        from pdi_copilot.journey import guidance, status_report
        store = Store(self.base / 'not-created')
        self.assertEqual(guidance(store)['stage'], 'setup_required')
        self.assertEqual(status_report(store)['status'], 'setup_required')
        self.assertFalse(store.root.exists())

    def test_empty_status_and_drafts_require_explicit_selection(self):
        from pdi_copilot.journey import guidance, status_report, guidance_text
        self.assertEqual(status_report(self.store)['status'], 'no_active_cycle')
        for cid in ('draft-a', 'draft-b'):
            create_cycle(self.store, cid, 'Rascunho fictício')
            result = status_report(self.store)
            self.assertIsNone(result['cycle_id'])
            self.assertEqual(result['onboarding']['stage'], 'cycle_selection')
        before = {p.relative_to(self.store.root): p.read_bytes()
                  for p in self.store.root.rglob('*') if p.is_file()}
        selected = status_report(self.store, 'draft-b')
        self.assertEqual(selected['status'], 'draft')
        self.assertEqual(selected['cycle_id'], 'draft-b')
        self.assertIn('draft-b', guidance_text(selected))
        self.assertIsNone(self.store.load()['active_cycle'])
        self.assertEqual(before, {p.relative_to(self.store.root): p.read_bytes()
                                 for p in self.store.root.rglob('*') if p.is_file()})
        with self.assertRaises(PDIError): guidance(self.store, 'missing')

    def test_onboarding_resumes_notes_proposals_and_applied_answers(self):
        from pdi_copilot.journey import guidance
        create_cycle(self.store, 'draft', 'Rascunho fictício')
        note = self.store.root / 'inbox/onboarding.md'
        note.write_text('Relato fictício: função Engenharia; senioridade Pleno. Data desconhecida.')
        proposal = prepare_proposal(self.store, [{'op': 'profile', 'value': {'role': 'Engenharia', 'seniority': 'Pleno'}}], 'Respostas fictícias')
        result = guidance(Store(self.store.root), 'draft')
        self.assertEqual(result['stage'], 'proposal_review')
        self.assertEqual(result['resume_notes'], [str(note)])
        self.assertEqual(result['pending_proposals'][0]['status'], 'awaiting_review')
        self.assertIsNone(result['profile']['role'])
        apply_proposal(self.store, proposal['proposal'], True)
        resumed = guidance(Store(self.store.root), 'draft')
        self.assertEqual(resumed['pending_proposals'], [])
        self.assertNotIn('role', resumed['missing_profile'])
        self.assertNotIn('seniority', resumed['missing_profile'])
        self.assertEqual(len(resumed['questions']), 2)
        self.assertEqual(note.read_text(), 'Relato fictício: função Engenharia; senioridade Pleno. Data desconhecida.')

    def test_onboarding_exposes_stale_and_broken_proposals(self):
        from pdi_copilot.journey import guidance
        proposal = prepare_proposal(self.store, [{'op': 'profile', 'value': {'role': 'Engenharia'}}], 'Candidato fictício')
        self.change([{'op': 'profile', 'value': {'area': 'Área fictícia'}}])
        result = guidance(self.store)
        self.assertEqual(result['pending_proposals'][0]['status'], 'stale')
        self.assertIsNone(result['profile']['role'])
        (self.store.root / 'proposals/broken.json').write_text('{broken')
        result = guidance(self.store)
        self.assertEqual(result['stage'], 'proposal_check_required')
        self.assertEqual(len(result['proposal_issues']), 1)
        self.assertTrue(Path(proposal['proposal']).exists())

    def test_onboarding_without_documents_can_reach_plan_building(self):
        from pdi_copilot.journey import guidance
        create_cycle(self.store, 'draft', 'Ciclo fictício', '2026-07-01', '2027-05-31', '2027-04-30')
        self.change([{'op': 'profile', 'value': {'role': 'Engenharia', 'seniority': 'Pleno',
                    'area': 'Área fictícia', 'career_goal': 'Objetivo fictício',
                    'weekly_capacity_hours': 0, 'timezone': 'UTC', 'leadership': False}}])
        result = guidance(self.store, 'draft')
        self.assertEqual(result['stage'], 'plan_building')
        self.assertEqual(result['missing_profile'], [])
        self.assertIn('pdi_closes_on', result['missing_calendar'])
        self.assertEqual(result['source_count'], 0)
        self.assertIn('opcionais', result['next_steps'][0])

    def test_status_cli_json_and_text_without_cycle(self):
        source = Path(__file__).resolve().parents[1]
        for command in ('onboarding', 'status'):
            for fmt in ('json', 'text'):
                result = subprocess.run([sys.executable, str(source / 'scripts/pdi.py'),
                    '--outtie', str(self.store.root), command, '--format', fmt],
                    check=True, capture_output=True, text=True)
                if fmt == 'json': self.assertEqual(json.loads(result.stdout)['revision'], 0)
                else: self.assertIn('Ciclo ativo: nenhum', result.stdout)

    def test_status_keeps_active_indicators_and_can_consult_archive(self):
        from pdi_copilot.journey import status_report
        self.new_cycle()
        self.action(effort_hours=None)
        state = self.store.load()
        result = status_report(self.store, on='2027-03-02')
        for key, value in overview(state, on='2027-03-02').items():
            self.assertEqual(result[key], value)
        self.assertEqual(result['onboarding']['stage'], 'tracking')
        close_cycle(self.store, 'cycle-1', self.innie, approved=True)
        self.assertEqual(status_report(self.store)['status'], 'no_active_cycle')
        self.assertEqual(status_report(self.store, 'cycle-1')['onboarding']['stage'], 'archived')

    def test_package_rejects_source_corruption_and_unknown_reference(self):
        source = Path(__file__).resolve().parents[1]
        package = self.base / 'package'
        # Funciona também numa distribuição sem .git; nunca copia o outtie/configuração.
        package.mkdir()
        for folder in ('.github', 'scripts', 'src', 'schemas', 'templates', 'docs', 'knowledge'):
            shutil.copytree(source / folder, package / folder, ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('README.md', 'INSTALL.md', 'AGENTS.md', 'CHANGELOG.md', 'pdi.code-workspace'):
            shutil.copyfile(source / name, package / name)
        def check():
            return subprocess.run([sys.executable, str(package / 'scripts/check_package.py'), '--distribution'], capture_output=True, text=True)
        result = check()
        self.assertEqual(result.returncode, 0, result.stderr)
        matrix = package / 'knowledge/competencies/devops.json'
        original = matrix.read_text(); matrix.write_text(original + ' ')
        result = check(); self.assertNotEqual(result.returncode, 0)
        self.assertIn('divergente: I07', result.stderr)
        matrix.write_text(original)
        summary = package / 'knowledge/policies/summary.md'
        summary.write_text(summary.read_text() + '\nFonte X99 não registrada.\n')
        result = check(); self.assertNotEqual(result.returncode, 0)
        self.assertIn('X99', result.stderr)

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
        connect(self.innie, self.store.root)
        before = self.store.load()
        with patch('pdi_copilot.cli.INNIE', self.innie):
            for _ in range(2):
                result = run(parser().parse_args(['--outtie', str(self.store.root), 'setup']))
                workspace = Path(result['workspace'])
                roots = [(workspace.parent / f['path']).resolve()
                         for f in read_json(workspace)['folders']]
                self.assertEqual(roots, [self.innie, self.store.root])
        self.assertEqual(self.store.load(), before)

    def test_setup_existing_space_requires_explicit_connection(self):
        target = Store(self.base / 'espaço existente'); target.initialize()
        before = {p.relative_to(target.root): p.read_bytes()
                  for p in target.root.rglob('*') if p.is_file()}
        with patch('pdi_copilot.cli.INNIE', self.innie):
            with self.assertRaises(PDIError) as error:
                run(parser().parse_args(['--outtie', str(target.root), 'setup']))
            command = shlex.join(['python3', 'scripts/pdi.py', '--outtie', str(target.root), 'connect'])
            self.assertIn(command, str(error.exception))
            self.assertFalse((self.innie / 'pessoal').is_symlink())
            self.assertFalse((self.innie / '.local').exists())
            self.assertEqual(before, {p.relative_to(target.root): p.read_bytes()
                                     for p in target.root.rglob('*') if p.is_file()})
            run(parser().parse_args(['--outtie', str(target.root), 'connect']))
            self.assertFalse(run(parser().parse_args(['setup']))['initialized'])
        self.assertEqual((self.innie / 'pessoal').resolve(), target.root)

    def test_setup_creates_new_space_and_reuses_its_binding(self):
        target = self.base / 'novo espaço'
        with patch('pdi_copilot.cli.INNIE', self.innie):
            self.assertTrue(run(parser().parse_args(['--outtie', str(target), 'setup']))['initialized'])
            before = Store(target).load()
            self.assertFalse(run(parser().parse_args(['setup']))['initialized'])
        self.assertEqual(Store(target).load(), before)
        self.assertEqual((self.innie / 'pessoal').resolve(), target)

    def test_setup_recovers_existing_binding_from_link_or_config(self):
        target = Store(self.base / 'custom-outtie'); target.initialize()
        before = target.load()
        for missing in ('pessoal', '.local/config.json'):
            with self.subTest(missing=missing):
                connect(self.innie, target.root)
                (self.innie / missing).unlink()
                with patch('pdi_copilot.cli.INNIE', self.innie):
                    result = run(parser().parse_args(['setup']))
                self.assertFalse(result['initialized'])
                self.assertEqual(Path(result['outtie']), target.root)
                self.assertEqual(target.load(), before)

    def test_unconfigured_commands_do_not_assume_existing_sibling(self):
        before = self.store.load()
        with patch('pdi_copilot.cli.INNIE', self.innie):
            for command in ('setup', 'state', 'doctor', 'connect'):
                with self.subTest(command=command), self.assertRaisesRegex(PDIError, 'sem vínculo'):
                    run(parser().parse_args([command]))
            # Um caminho fornecido explicitamente permite inspeção sem criar vínculo.
            self.assertEqual(run(parser().parse_args(['--outtie', str(self.store.root), 'state'])), before)
        self.assertFalse((self.innie / 'pessoal').is_symlink())
        self.assertFalse((self.innie / '.local').exists())
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
        connect(self.innie, self.store.root)
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
        connect(self.innie, self.store.root)
        before = self.store.load()
        for _ in range(2):
            result = subprocess.run(['bash', str(self.innie / 'scripts/bootstrap.sh')],
                                    cwd=self.base, check=True, capture_output=True, text=True)
            self.assertIn('Preparação local concluída.', result.stdout)
            self.assertIn('Espaço individual já conectado.', result.stdout)
            self.assertIn('/pdi-iniciar', result.stdout)
            workspace = self.innie / '.local/pdi.code-workspace'
            self.assertIn(str(workspace), result.stdout)
            self.assertEqual([(workspace.parent / f['path']).resolve()
                              for f in read_json(workspace)['folders']], [self.innie, self.store.root])
        shared = read_json(self.innie / 'pdi.code-workspace')
        self.assertEqual([(self.innie / f['path']).resolve() for f in shared['folders']],
                         [self.innie, self.store.root])
        result = subprocess.run(['bash', str(self.innie / 'scripts/bootstrap.sh'), 'state'],
                                cwd=self.base, check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), before)
        result = subprocess.run(['bash', str(self.innie / 'scripts/bootstrap.sh'), 'setup', '--format', 'json'],
                                cwd=self.base, check=True, capture_output=True, text=True)
        self.assertTrue(json.loads(result.stdout)['local_ready'])

    def test_new_sibling_installation_requires_connect_after_bootstrap(self):
        source = Path(__file__).resolve().parents[1]
        parent = self.base / 'instalações novas'; parent.mkdir()
        first = parent / 'innie'; second = parent / 'outro-clone'
        for installation in (first, second):
            installation.mkdir()
            shutil.copytree(source / 'scripts', installation / 'scripts')
            shutil.copytree(source / 'src', installation / 'src')
        def bootstrap(installation, *args):
            return subprocess.run(['bash', str(installation / 'scripts/bootstrap.sh'), *args],
                                  cwd=installation, capture_output=True, text=True)
        created = bootstrap(first)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertIn('Espaço individual criado.', created.stdout)
        original = Store(parent / 'outtie'); before = original.load()
        refused = bootstrap(second)
        self.assertEqual(refused.returncode, 2)
        self.assertIn(str(original.root), json.loads(refused.stderr)['error'])
        self.assertFalse((second / 'pessoal').is_symlink())
        self.assertFalse((second / '.local').exists())
        self.assertEqual(original.load(), before)
        connected = bootstrap(second, '--outtie', str(original.root), 'connect')
        self.assertEqual(connected.returncode, 0, connected.stderr)
        for installation in (first, second):
            repeated = bootstrap(installation)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertIn('Espaço individual já conectado.', repeated.stdout)
        self.assertEqual(original.load(), before)

    def test_preparation_guides_custom_workspace_without_optional_tools(self):
        target = self.base / 'novo espaço com acentos'
        actual_which = shutil.which
        def required_only(tool):
            return actual_which(tool) if tool == 'git' else None
        with patch('pdi_copilot.cli.INNIE', self.innie), patch('pdi_copilot.operations.shutil.which', side_effect=required_only):
            result = run(parser().parse_args(['--outtie', str(target), 'setup']))
        self.assertTrue(result['initialized'])
        self.assertTrue(result['local_ready'])
        self.assertEqual(result['copilot_context'], 'manual_check_required')
        self.assertEqual(result['context_to_verify'], {'revision': 0, 'active_cycle': None})
        self.assertIn('Arquivo > Abrir Workspace', result['next_steps'][1])
        self.assertIn(str(self.innie / '.local/pdi.code-workspace'), result['next_steps'][1])
        self.assertIn('copiloto-desenvolvimento', result['next_steps'][2])
        self.assertIn('/pdi-iniciar', result['next_steps'][-1])

    def test_preparation_quotes_workspace_command_with_spaces(self):
        installation = self.base / 'núcleo com espaços'; installation.mkdir()
        target = self.base / 'outtie com espaços'
        with patch('pdi_copilot.cli.INNIE', installation), patch('pdi_copilot.operations.shutil.which', return_value='/synthetic/tool'):
            result = run(parser().parse_args(['--outtie', str(target), 'setup']))
        command = result['next_steps'][1].removeprefix('Abra o workspace: ')
        self.assertEqual(shlex.split(command), ['code', str(installation / '.local/pdi.code-workspace')])
        self.assertEqual(shlex.split(result['next_steps'][0].removeprefix('Confira o ambiente: ')),
                         ['python3', str(installation / 'scripts/pdi.py'), 'doctor'])

    def test_missing_git_blocks_preparation_before_creating_files(self):
        target = self.base / 'missing-git'
        with patch('pdi_copilot.cli.INNIE', self.innie), patch('pdi_copilot.operations.shutil.which', return_value=None):
            with self.assertRaisesRegex(PDIError, 'Git ausente'):
                run(parser().parse_args(['--outtie', str(target), 'setup']))
        self.assertFalse(target.exists())
        self.assertFalse((self.innie / '.local').exists())

    def test_old_python_blocks_preparation_before_creating_files(self):
        target = self.base / 'old-python'
        with patch('pdi_copilot.cli.INNIE', self.innie), patch('pdi_copilot.operations.sys.version_info', (3, 10, 0)):
            with self.assertRaisesRegex(PDIError, 'Python 3.11'):
                run(parser().parse_args(['--outtie', str(target), 'setup']))
        self.assertFalse(target.exists())
        self.assertFalse((self.innie / '.local').exists())

    def test_doctor_before_setup_explains_next_step_without_creating_state(self):
        store = Store(self.base / 'not-created')
        result = doctor(self.innie, store)
        self.assertFalse(result['ok'])
        self.assertEqual(result['state'], 'not_initialized')
        self.assertTrue(result['setup_required'])
        self.assertIn('bootstrap.sh', result['next'])
        self.assertIn('environment', result)
        self.assertFalse(store.root.exists())

    def test_doctor_corrupt_state_preserves_files_and_routes_recovery(self):
        revision = self.store.root / 'revisions/00000000.json'; revision.write_text('{}')
        result = doctor(self.innie, self.store)
        self.assertFalse(result['ok'])
        self.assertEqual(result['state'], 'error')
        self.assertFalse(result['setup_required'])
        self.assertIn('troubleshooting', result['next'])
        self.assertEqual(revision.read_text(), '{}')

    def test_bootstrap_without_python_explains_installation(self):
        commands = self.base / 'commands'; commands.mkdir()
        (commands / 'dirname').symlink_to(shutil.which('dirname'))
        source = Path(__file__).resolve().parents[1]
        result = subprocess.run([shutil.which('bash'), str(source / 'scripts/bootstrap.sh')],
                                env={**os.environ, 'PATH': str(commands)}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Python 3 ausente', result.stderr)
        self.assertIn('--install-deps', result.stderr)

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

    def test_new_profile_and_cycle_do_not_presume_personal_answers(self):
        self.assertTrue(all(value is None for value in self.store.load()['profile'].values()))
        self.new_cycle()
        c = cycle(self.store.load())
        self.assertEqual(c['evidence_cutoff_on'], '2027-04-30')
        self.assertIsNone(c['pdi_closes_on'])
        self.change([{'op': 'calendar', 'value': {'pdi_closes_on': '2027-04-20'}}])
        self.assertEqual(cycle(self.store.load())['evidence_cutoff_on'], '2027-04-30')
        self.assertEqual(cycle(self.store.load())['pdi_closes_on'], '2027-04-20')

    def test_unknown_effort_persists_and_renders_as_pending(self):
        self.new_cycle()
        self.change([
            {'op': 'profile', 'value': {'weekly_capacity_hours': 10}},
            *[{'op': 'upsert', 'collection': 'actions', 'value':
               {'id': aid, 'title': aid, 'status': 'planned', **fields}}
              for aid, fields in [('missing', {}), ('unknown', {'effort_hours': None}),
                                  ('zero', {'effort_hours': 0}), ('known', {'effort_hours': 2})]]
        ])
        before = self.store.load()
        report = overview(before, on='2027-04-23')
        self.assertIsNone(report['estimated_remaining_effort_hours'])
        self.assertEqual(report['known_remaining_effort_hours'], 2)
        self.assertEqual(report['actions_missing_effort'], ['missing', 'unknown'])
        self.assertIsNone(report['over_capacity'])
        render(self.store)
        outputs = self.store.root / 'cycles/cycle-1/outputs'
        plan = (outputs / 'plano.md').read_text()
        self.assertIn('| missing | missing | planned | pendente | pendente |', plan)
        self.assertIn('| unknown | unknown | planned | pendente | pendente |', plan)
        self.assertIn('| zero | zero | planned | pendente | 0 h |', plan)
        self.assertIn('Fechamento do PDI: pendente', plan)
        dashboard = (outputs / 'painel.md').read_text()
        self.assertIn('Esforço restante total: pendente', dashboard)
        self.assertIn('estimativas informadas: 2 horas', dashboard)
        self.assertIn('Ações sem estimativa de esforço: missing, unknown', dashboard)
        self.assertEqual(self.store.load(), before)
        archive = self.base / 'unknowns.zip'; backup(self.store, archive)
        restored = self.base / 'restored'; restore(archive, restored)
        self.assertEqual(Store(restored).load(), before)

    def test_capacity_distinguishes_unknown_zero_and_known_overload(self):
        self.new_cycle()
        cases = [
            # Esforços, capacidade semanal, total, soma conhecida, sobrecarga.
            ([], 10, 0, 0, False),
            ([None], 10, None, 0, None),
            ([0], 10, 0, 0, False),
            ([8], 10, 8, 8, False),
            ([9], 10, 9, 9, True),
            ([2, None], 10, None, 2, None),
            ([9, None], 10, None, 9, True),
            ([2], None, 2, 2, None),
            ([0], 0, 0, 0, False),
            ([None], 0, None, 0, None),
            ([2, None], 0, None, 2, True),
        ]
        for efforts, capacity, total, known, overloaded in cases:
            with self.subTest(efforts=efforts, capacity=capacity):
                state = self.store.load()
                state['profile']['weekly_capacity_hours'] = capacity
                cycle(state)['actions'] = [
                    {'id': f'a{i}', 'title': 'Fictícia', 'status': 'planned', 'effort_hours': value}
                    for i, value in enumerate(efforts)]
                report = overview(validate(state), on='2027-04-23')
                self.assertEqual(report['estimated_remaining_effort_hours'], total)
                self.assertEqual(report['known_remaining_effort_hours'], known)
                self.assertIs(report['over_capacity'], overloaded)
        state['active_cycle'] = None
        cycle(state, 'cycle-1').update(status='draft', evidence_cutoff_on=None)
        report = overview(validate(state), 'cycle-1', on='2027-04-23')
        self.assertIsNone(report['over_capacity'])
        self.assertIsNone(report['suggested_available_hours_with_20pct_margin'])

    def test_only_planned_and_in_progress_effort_enters_capacity(self):
        self.new_cycle()
        statuses = ['proposed', 'done', 'suspended', 'cancelled', 'carried_over', 'in_progress']
        self.change([{'op': 'upsert', 'collection': 'actions', 'value':
                      {'id': status, 'title': status, 'status': status}}
                     for status in statuses])
        report = overview(self.store.load(), on='2027-04-23')
        self.assertEqual(report['actions_missing_effort'], ['in_progress'])
        self.change([{'op': 'upsert', 'collection': 'actions',
                      'value': {'id': 'in_progress', 'effort_hours': 0}}])
        report = overview(self.store.load(), on='2027-04-23')
        self.assertEqual(report['actions_missing_effort'], [])
        self.assertEqual(report['estimated_remaining_effort_hours'], 0)

    def test_invalid_effort_is_still_rejected(self):
        self.new_cycle()
        before = self.store.load()
        for value in (-1, float('inf'), float('nan'), True, '2'):
            with self.subTest(value=value), self.assertRaises(PDIError):
                self.action(effort_hours=value)
        self.assertEqual(self.store.load(), before)

    def test_timezone_fallback_is_disclosed_without_filling_profile(self):
        self.new_cycle()
        before = self.store.load()
        report = overview(before)
        self.assertEqual(report['reference_timezone'], 'America/Fortaleza')
        self.assertTrue(report['reference_timezone_assumed'])
        render(self.store)
        panel = self.store.root / 'cycles/cycle-1/outputs/painel.md'
        self.assertIn('Fuso horário provisório do piloto', panel.read_text())
        self.assertEqual(self.store.load(), before)
        explicit = overview(before, on='2027-04-23')
        self.assertEqual(explicit['reference_on'], '2027-04-23')
        self.assertIsNone(explicit['reference_timezone'])
        self.assertFalse(explicit['reference_timezone_assumed'])
        self.change([{'op': 'profile', 'value': {'timezone': 'UTC'}}])
        report = overview(self.store.load())
        self.assertEqual(report['reference_timezone'], 'UTC')
        self.assertFalse(report['reference_timezone_assumed'])
        with self.assertRaises(PDIError):
            self.change([{'op': 'profile', 'value': {'timezone': 'Invalid/Zone'}}])

    def test_existing_profile_calendar_and_zero_effort_are_preserved(self):
        self.new_cycle(); self.action(effort_hours=0)
        self.change([
            {'op': 'profile', 'value': {'role': 'DevOps', 'area': 'Operação',
                                      'leadership': False, 'timezone': 'America/Fortaleza'}},
            {'op': 'calendar', 'value': {'pdi_closes_on': '2027-04-30'}}])
        before = self.store.load()
        self.assertFalse(self.store.initialize())
        render(self.store)
        self.assertEqual(self.store.load(), before)
        self.assertEqual(overview(before)['estimated_remaining_effort_hours'], 0)

    def test_criteria_exposes_unknown_area_before_selecting_operation_rules(self):
        args = parser().parse_args(['--outtie', str(self.store.root), 'criteria'])
        report = run(args)
        self.assertTrue(report['area_pending'])
        self.assertTrue(all(row['scope'] == 'all' for row in report['criteria']))
        self.change([{'op': 'profile', 'value': {'area': 'Operação'}}])
        report = run(args)
        self.assertFalse(report['area_pending'])
        self.assertTrue(any(row['scope'] == 'Operação' for row in report['criteria']))

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
