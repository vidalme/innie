"""Revisões imutáveis com publicação atômica do ponteiro e lock POSIX."""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile

from .model import PDIError, SCHEMA, blank_state, now, validate

def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")

def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PDIError(f"Não foi possível ler JSON: {path}: {exc}") from exc

def atomic(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def write_json(path, obj):
    atomic(path, json_bytes(obj))

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def inside(root, path):
    root, target = Path(root).resolve(), Path(path).resolve()
    if not target.is_relative_to(root):
        raise PDIError(f"Caminho fora do espaço permitido: {path}")
    return target

class Store:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()

    def ensure_folders(self):
        for folder in ["revisions", "sources/originals", "sources/extracted", "evidence/files", "inbox", "cycles", "archives", "proposals", "exports", "operations", "backups"]:
            inside(self.root, self.root / folder).mkdir(parents=True, exist_ok=True)

    @contextmanager
    def lock(self):
        lockpath = inside(self.root, self.root / ".runtime/lock")
        lockpath.parent.mkdir(parents=True, exist_ok=True)
        with lockpath.open("a+") as stream:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise PDIError("Outra operação está usando este outtie. Tente novamente depois.") from exc
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def initialize(self):
        self.root.mkdir(parents=True, exist_ok=True)
        with self.lock():
            if (self.root / "metadata.json").exists():
                self.load(); self.ensure_folders(); return False
            allowed = {"README.md", ".gitignore", ".git", ".gitkeep", ".runtime"}
            if any(p.name not in allowed for p in self.root.iterdir()):
                raise PDIError("Pasta preenchida sem metadados. Preserve-a e use importação assistida em um novo outtie.")
            self.ensure_folders()
            state = blank_state()
            write_json(self.root / "revisions/00000000.json", state)
            write_json(self.root / "metadata.json", {"schema_version": SCHEMA, "revision": 0,
                       "sha256": digest(self.root / "revisions/00000000.json"), "created_at": now()})
        return True

    def load(self):
        meta = read_json(inside(self.root, self.root / "metadata.json"))
        if meta.get("schema_version") != SCHEMA or type(meta.get("revision")) is not int or meta["revision"] < 0:
            raise PDIError("Formato não suportado; faça backup e consulte a migração.")
        path = inside(self.root, self.root / f"revisions/{meta['revision']:08d}.json")
        if digest(path) != meta.get("sha256"):
            raise PDIError("Hash da revisão divergente. Não editar revisions manualmente; utilize restauração.")
        state = validate(read_json(path))
        if state["revision"] != meta["revision"]:
            raise PDIError("Revisão inconsistente.")
        return state

    def commit(self, candidate, expected, reason, actor="user"):
        """Chamador deve manter lock até terminar sua operação."""
        current = self.load()
        if current["revision"] != expected:
            raise PDIError("Conflito de versão: reavalie a proposta contra o estado atual.")
        candidate["revision"] = expected + 1
        candidate["updated_at"] = now()
        candidate["changes"].append({"revision": expected + 1, "reason": reason, "actor": actor, "at": now()})
        validate(candidate)
        path = inside(self.root, self.root / f"revisions/{expected+1:08d}.json")
        # Uma revisão órfã pode existir depois de falha antes da troca de ponteiro.
        if path.exists():
            orphan = inside(self.root, self.root / f"operations/orphan-{expected+1:08d}-{os.urandom(4).hex()}.json")
            os.replace(path, orphan)
        write_json(path, candidate)
        oldmeta = read_json(self.root / "metadata.json")
        write_json(self.root / "metadata.json", {**oldmeta, "revision": expected+1, "sha256": digest(path)})
        return candidate
