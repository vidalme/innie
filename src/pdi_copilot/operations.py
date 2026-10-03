"""Preparação, propostas, fontes, arquivos de ciclos e backups."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

from .model import PDIError, apply_operations, blank_cycle, cycle, date, find, new_id, now, valid_id, validate
from .storage import Store, atomic, digest, inside, json_bytes, read_json, write_json

def git_check(innie):
    innie = Path(innie).resolve()
    if not (innie / ".git").exists():
        return {"status": "not_initialized", "tracked_private": []}
    result = subprocess.run(["git", "-C", str(innie), "ls-files", "-z"], capture_output=True, check=True)
    private = [x for x in result.stdout.decode().split("\0") if x == "pessoal" or x.startswith(("pessoal/", ".local/"))]
    ignored = subprocess.run(["git", "-C", str(innie), "check-ignore", "pessoal"], capture_output=True).returncode == 0
    return {"status": "error" if private or not ignored else "ok", "tracked_private": private, "pessoal_ignored": ignored}

def connect(innie, outtie, switch=False, two_roots=False):
    innie = Path(innie).expanduser().resolve()
    root = Path(outtie).expanduser().resolve()
    if root == innie or root.is_relative_to(innie) or innie.is_relative_to(root) or ".git" in root.parts:
        raise PDIError("Innie e outtie devem ser pastas distintas, sem conter uma à outra.")
    store = Store(root); store.load()
    link = innie / "pessoal"
    if link.exists() or link.is_symlink():
        if not link.is_symlink():
            raise PDIError("pessoal é uma pasta/arquivo real. Faça backup e migração explícita antes de criar o link.")
        if link.resolve() != root and not switch:
            raise PDIError("Outro outtie está conectado. Use --switch após revisar o destino.")
    ignored = git_check(innie)
    if ignored["status"] == "error":
        raise PDIError("O Git do innie inclui conteúdo individual ou não ignora pessoal. Corrija antes de conectar.")
    if not link.is_symlink() or link.resolve() != root:
        temporary = innie / (".pessoal-" + os.urandom(4).hex())
        temporary.symlink_to(os.path.relpath(root, innie), target_is_directory=True)
        os.replace(temporary, link)
    local = innie / ".local"
    local.mkdir(exist_ok=True)
    write_json(local / "config.json", {"outtie": str(root), "connected_at": now(), "two_roots": two_roots})
    folders = [{"name": "Innie", "path": "."}]
    if two_roots:
        folders.append({"name": "Meu desenvolvimento", "path": os.path.relpath(root, innie)})
    workspace = {"folders": folders, "settings": {"files.exclude": {"**/__pycache__": True}},
                 "extensions": {"recommendations": ["ms-vscode-remote.remote-wsl", "github.copilot", "github.copilot-chat"]}}
    write_json(innie / ".local/pdi.code-workspace", workspace)
    # Workspace em .local usa caminhos relativos a .local, não à raiz.
    workspace["folders"][0]["path"] = ".."
    if two_roots:
        workspace["folders"][1]["path"] = os.path.relpath(root, local)
    write_json(local / "pdi.code-workspace", workspace)
    return {"outtie": str(root), "symlink": str(link), "workspace": str(local / "pdi.code-workspace")}

def doctor(innie, store):
    state = store.load()
    innie = Path(innie).resolve()
    checks = {"state": "ok", "revision": state["revision"], "outtie": str(store.root),
              "symlink": (innie / "pessoal").is_symlink() and (innie / "pessoal").resolve() == store.root,
              "git": git_check(innie), "wsl_detected": "microsoft" in os.uname().release.lower(),
              "python": os.sys.version.split()[0], "optional_tools": {x: shutil.which(x) is not None for x in ["git", "code", "pdftotext", "tesseract"]}}
    with store.lock():
        testfile = inside(store.root, store.root / ".runtime/doctor.txt")
        atomic(testfile, b"pdi-doctor")
        linked = innie / "pessoal/.runtime/doctor.txt"
        checks["filesystem_link_read"] = checks["symlink"] and linked.read_bytes() == b"pdi-doctor"
        testfile.unlink()
    checks["copilot_context"] = "manual_check_required"
    checks["ok"] = checks["symlink"] and checks["filesystem_link_read"] and checks["git"]["status"] != "error"
    return checks

def prepare_proposal(store, changes, reason):
    if not reason.strip():
        raise PDIError("Informe o motivo da proposta.")
    with store.lock():
        state = store.load()
        apply_operations(state, changes)
        proposal = {"schema_version": 1, "id": new_id("proposal"), "expected_revision": state["revision"],
                    "created_at": now(), "reason": reason, "operations": changes}
        path = inside(store.root, store.root / f"proposals/{proposal['id']}.json")
        write_json(path, proposal)
    return {"proposal": str(path), "expected_revision": state["revision"], "operations": len(changes), "review_required": True}

def apply_proposal(store, proposal_path, approved=False):
    if not approved:
        raise PDIError("Revise a proposta; use --approve somente após autorização para aplicá-la.")
    path = inside(store.root / "proposals", proposal_path)
    proposal = read_json(path)
    valid_id(proposal.get("id"))
    if proposal.get("schema_version") != 1:
        raise PDIError("Formato de proposta inválido.")
    with store.lock():
        state = store.load()
        if state["revision"] != proposal["expected_revision"]:
            raise PDIError("Proposta desatualizada. Recrie-a com o estado atual.")
        candidate = apply_operations(state, proposal["operations"])
        result = store.commit(candidate, state["revision"], proposal["reason"])
        write_json(inside(store.root, store.root / f"operations/{proposal['id']}.json"),
                   {"proposal_id": proposal["id"], "applied_revision": result["revision"], "at": now()})
    return {"revision": result["revision"], "proposal_id": proposal["id"], "render_next": True}

def create_cycle(store, cycle_id, label, starts_on=None, ends_on=None, cutoff_on=None, evaluation_on=None):
    with store.lock():
        state = store.load()
        existing = next((c for c in state["cycles"] if c["id"] == cycle_id), None)
        if existing:
            return {"id": cycle_id, "created": False, "status": existing["status"]}
        candidate = copy.deepcopy(state)
        candidate["cycles"].append(blank_cycle(cycle_id, label, starts_on, ends_on, cutoff_on, evaluation_on))
        result = store.commit(candidate, state["revision"], f"Criar ciclo {cycle_id}")
    return {"id": cycle_id, "created": True, "revision": result["revision"], "status": "draft"}

def start_cycle(store, cycle_id, reviewed=False):
    if not reviewed:
        raise PDIError("Revise calendário, regras e contexto e informe --reviewed para ativar.")
    with store.lock():
        state = store.load()
        if state["active_cycle"] == cycle_id:
            return {"id": cycle_id, "started": False}
        if state["active_cycle"]:
            raise PDIError("Encerre o ciclo ativo antes de ativar outro.")
        candidate = copy.deepcopy(state); c = cycle(candidate, cycle_id)
        if c["status"] != "draft":
            raise PDIError("Só é possível ativar um ciclo em rascunho.")
        c["status"] = "active"; candidate["active_cycle"] = cycle_id
        result = store.commit(candidate, state["revision"], f"Ativar ciclo revisado {cycle_id}")
    return {"id": cycle_id, "started": True, "revision": result["revision"]}

def import_source(store, file, kind="personal", title=None):
    file = Path(file).expanduser().resolve()
    if not file.is_file():
        raise PDIError("Fonte precisa ser arquivo regular existente.")
    fingerprint = digest(file)
    with store.lock():
        state = store.load()
        existing = next((s for s in state["sources"] if s.get("sha256") == fingerprint), None)
        if existing:
            return {"id": existing["id"], "imported": False, "duplicate": True}
        source_id = new_id("source")
        safe_name = re.sub(r"[^\w.()-]", "_", file.name)[:120] or "fonte"
        rel = f"sources/originals/{source_id}--{safe_name}"
        target = inside(store.root, store.root / rel)
        atomic(target, file.read_bytes())
        extracted = None
        if file.suffix.lower() in {".md", ".txt", ".json", ".csv", ".html", ".htm"}:
            extracted = file.read_text(encoding="utf-8", errors="replace")
            if file.suffix.lower() in {".html", ".htm"}:
                from html.parser import HTMLParser
                class Text(HTMLParser):
                    def __init__(self): super().__init__(); self.parts=[]; self.skip=0
                    def handle_starttag(self, tag, attrs):
                        if tag in {"script", "style"}: self.skip += 1
                        if tag in {"tr", "td", "p", "br", "li", "h1", "h2"}: self.parts.append("\n")
                    def handle_endtag(self, tag):
                        if tag in {"script", "style"}: self.skip -= 1
                    def handle_data(self, data):
                        if not self.skip: self.parts.append(data)
                parser = Text(); parser.feed(extracted); extracted = "".join(parser.parts)
        elif file.suffix.lower() == ".pdf" and shutil.which("pdftotext"):
            command = subprocess.run(["pdftotext", "-layout", str(target), "-"], capture_output=True)
            if command.returncode == 0:
                extracted = command.stdout.decode("utf-8", errors="replace")
        text_rel = None
        if extracted and extracted.strip():
            text_rel = f"sources/extracted/{source_id}.txt"
            atomic(inside(store.root, store.root / text_rel), extracted.encode("utf-8"))
        row = {"id": source_id, "kind": kind, "title": title or file.name,
               "original_name": file.name, "local_path": rel, "sha256": fingerprint,
               "extracted_path": text_rel, "extraction_status": "available" if text_rel else "manual_required",
               "imported_at": now()}
        candidate = copy.deepcopy(state); candidate["sources"].append(row)
        store.commit(candidate, state["revision"], f"Importar fonte {source_id}")
    return {"id": source_id, "imported": True, "source": rel, "extracted_path": text_rel, "next": "Revisar conteúdo; importação não confirma fatos ou critérios."}

def manifest(directory, exclude=None):
    directory = Path(directory)
    files = {}
    for path in sorted(directory.rglob("*")):
        rel = path.relative_to(directory)
        if exclude and any(part in exclude for part in rel.parts):
            continue
        if path.is_symlink():
            raise PDIError(f"Não copiar symlink no espaço individual: {rel}")
        if path.is_file():
            files[rel.as_posix()] = digest(path)
    return files

def close_cycle(store, cycle_id, innie, approved=False):
    if not approved:
        raise PDIError("Revise o fechamento e use --approve.")
    with store.lock():
        state = store.load(); original = cycle(state, cycle_id)
        if original["status"] == "archived":
            return {"id": cycle_id, "closed": False, "archive": original["archive_path"]}
        if original["status"] != "active":
            raise PDIError("Somente o ciclo ativo pode ser fechado.")
        candidate = copy.deepcopy(state); c = cycle(candidate, cycle_id)
        label = f"{c['starts_on']}_a_{c['ends_on']}__{cycle_id}"
        rel = "archives/" + label
        target = inside(store.root, store.root / rel)
        c.update({"status": "archived", "closed_at": now(), "archive_path": rel})
        candidate["active_cycle"] = None
        validate(candidate)
        if target.exists():
            receipt = read_json(target / "MANIFEST.json")
            if receipt.get("source_revision") != state["revision"]:
                raise PDIError("Arquivo existente não corresponde ao estado atual. Examine recuperação antes de fechar.")
            verify_archive(target)
        else:
            staging = Path(tempfile.mkdtemp(prefix=".closing-", dir=store.root / "archives"))
            try:
                write_json(staging / "cycle.json", c)
                write_json(staging / "profile-at-close.json", state["profile"])
                source_ids = set()
                evidence_ids = set()
                for key in ["actions", "events", "competency_assessments", "metrics", "objectives", "criterion_assessments"]:
                    for row in c[key]:
                        source_ids.update(row.get("source_ids", [])); evidence_ids.update(row.get("evidence_ids", []))
                for row in c["criterion_assessments"]:
                    evidence_ids.update(row.get("evidence_ids", []))
                ev = [x for x in state["evidence"] if x["id"] in evidence_ids]
                for row in ev: source_ids.update(row.get("source_ids", []))
                sources = [x for x in state["sources"] if x["id"] in source_ids]
                write_json(staging / "evidence.json", ev); write_json(staging / "sources.json", sources)
                for row in [*sources, *ev]:
                    for key in ["local_path", "extracted_path"]:
                        if row.get(key):
                            src = inside(store.root, store.root / row[key])
                            if not src.is_file():
                                raise PDIError(f"Arquivo de evidência/fonte ausente: {row[key]}")
                            dest = inside(staging, staging / row[key]); dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src, dest)
                knowledge = Path(innie).resolve() / "knowledge"
                if knowledge.exists():
                    shutil.copytree(knowledge, staging / "institutional-snapshot")
                outputs = store.root / "cycles" / cycle_id / "outputs"
                if outputs.exists():
                    shutil.copytree(outputs, staging / "outputs")
                hashes = manifest(staging)
                write_json(staging / "MANIFEST.json", {"cycle_id": cycle_id, "source_revision": state["revision"], "files": hashes,
                           "external_links_not_downloaded": True, "created_at": now()})
                verify_archive(staging)
                os.replace(staging, target)
            finally:
                if staging.exists(): shutil.rmtree(staging)
        store.commit(candidate, state["revision"], f"Arquivar ciclo {cycle_id}")
    return {"id": cycle_id, "closed": True, "archive": rel}

def verify_archive(path):
    path = Path(path).resolve()
    receipt = read_json(path / "MANIFEST.json")
    actual = manifest(path)
    actual.pop("MANIFEST.json", None)
    if actual != receipt.get("files"):
        raise PDIError("Manifesto do arquivo de ciclo não confere.")
    return {"verified": True, "files": len(actual)}

def backup(store, destination):
    destination = Path(destination).expanduser().resolve()
    if destination.is_relative_to(store.root) or destination.exists():
        raise PDIError("Backup deve ser um arquivo novo fora do outtie.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with store.lock():
        store.load()
        files = manifest(store.root, exclude={".git", ".runtime", "backups", "__pycache__"})
        provenance = store.root / ".runtime/views.json"
        if provenance.is_file():
            files[".runtime/views.json"] = digest(provenance)
        fd, tmp = tempfile.mkstemp(prefix=".backup-", dir=destination.parent); os.close(fd)
        try:
            with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
                for name in files: z.write(store.root / name, name)
                z.writestr("BACKUP_MANIFEST.json", json_bytes({"schema_version": 1, "files": files, "created_at": now()}))
            with zipfile.ZipFile(tmp) as z:
                if z.testzip(): raise PDIError("Falha de integridade no backup.")
            os.replace(tmp, destination)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
    return {"backup": str(destination), "files": len(files), "sha256": digest(destination)}

def restore(backup_file, destination):
    destination = Path(destination).expanduser().resolve()
    if destination.exists():
        raise PDIError("Restaurar exige destino inexistente; a cópia atual não será sobrescrita.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".restoring-", dir=destination.parent))
    try:
        with zipfile.ZipFile(backup_file) as z:
            names = z.namelist()
            if len(names) != len(set(names)) or sum(x.file_size for x in z.infolist()) > 512 * 1024 * 1024:
                raise PDIError("Backup duplicado ou maior que o limite de 512 MiB.")
            for info in z.infolist():
                if "\\" in info.filename or info.filename.startswith("/") or ".." in Path(info.filename).parts or ((info.external_attr >> 16) & 0o170000) == 0o120000:
                    raise PDIError("Caminho/link não permitido no backup.")
            receipt = json.loads(z.read("BACKUP_MANIFEST.json"))
            if set(names) != set(receipt["files"]) | {"BACKUP_MANIFEST.json"}:
                raise PDIError("Conteúdo do backup difere do manifesto.")
            for name, expected in receipt["files"].items():
                path = inside(stage, stage / name)
                atomic(path, z.read(name))
                if digest(path) != expected: raise PDIError("Hash incorreto no backup.")
        Store(stage).initialize()
        os.replace(stage, destination)
    finally:
        if stage.exists(): shutil.rmtree(stage)
    return {"restored": str(destination), "next": "Use connect para ligar o espaço restaurado ao innie."}

def init_git(store, innie=False):
    if not shutil.which("git"): raise PDIError("Git não encontrado.")
    root = store.root if isinstance(store, Store) else Path(store).resolve()
    if (root / ".git").exists(): return {"initialized": False, "path": str(root)}
    subprocess.run(["git", "init", "--initial-branch=main", str(root)], check=True, capture_output=True)
    return {"initialized": True, "path": str(root), "remote_created": False, "files_staged": False}
