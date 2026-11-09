"""Tira o próximo vídeo pronto de videos/fila/ (NN-nome.mp4 + NN-nome.json com a legenda) e coloca em posts/fila/ como Reels.
Roda pelo workflow "Vídeo do dia" (GitHub Actions), que depois envia ao GitHub e chama o publicar.py."""
import json
import shutil
import time
from pathlib import Path

ORIGEM, FILA = Path("videos/fila"), Path("posts/fila")


def main():
    pendentes = sorted(ORIGEM.glob("*.json"))
    if not pendentes:
        print("Fila de vídeos vazia.")
        return
    dados = json.loads(pendentes[0].read_text(encoding="utf-8"))
    nome = time.strftime("%Y-%m-%d-%Hh%M", time.gmtime(time.time() - 3 * 3600)) + "-reels"
    FILA.mkdir(parents=True, exist_ok=True)
    shutil.move(str(pendentes[0].with_suffix(".mp4")), FILA / f"{nome}.mp4")
    (FILA / f"{nome}.json").write_text(json.dumps({"tipo": "reels", "video": f"posts/fila/{nome}.mp4", "legenda": dados["legenda"],
                                                   "titulo": dados.get("titulo", ""), "criado_em": int(time.time())}, ensure_ascii=False, indent=2), encoding="utf-8")
    pendentes[0].unlink()
    print("Na fila para publicar:", dados.get("titulo"), "->", nome)


if __name__ == "__main__":
    main()
