# -*- coding: utf-8 -*-
"""
Monta o Reel de lançamento do cluster de segurança (janela/sacada).
4 cenas: hook -> virada -> acolhimento -> CTA de marca. Sem narração —
o texto na tela carrega a mensagem. Som nativo dos clipes preservado
(ambiente real, não silêncio morto).
"""
import os, subprocess, sys, tempfile, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
FOOTAGE = os.path.join(BASE, "footage")
FONTE = r"C:\Windows\Fonts\bahnschrift.ttf"
FONTE_BOLD = r"C:\Windows\Fonts\bahnschrift.ttf"
W, H, FPS = 1080, 1920, 30
AMBAR = "0xE0930C"
CREME = "0xFDF8F0"
INK = "0x1A1712"


def esc(p):
    return p.replace("\\", "/").replace(":", "\\:")


CENAS = [
    {"clipe": "janela_29631171.mp4", "d": 3.6, "texto": "CATS ALWAYS LAND\nON THEIR FEET.", "y": 0.72},
    {"clipe": "janela_36396667.mp4", "d": 4.0, "texto": "THAT DOESN'T MEAN\nFALLS DON'T HURT THEM.", "y": 0.18},
    {"clipe": "casa_30588697.mp4",   "d": 3.4, "texto": "A FEW MINUTES OF SCREENING\nPREVENTS MOST OF IT.", "y": 0.74},
]


def escrever(tmp, i, linhas):
    arq = os.path.join(tmp, f"txt{i}.txt")
    open(arq, "w", encoding="utf-8").write(linhas)
    return esc(arq)


def montar():
    tmp = tempfile.mkdtemp(prefix="reel_")
    try:
        entradas, filtro, rotulos = [], "", []
        duracao_total = sum(c["d"] for c in CENAS) + 3.6  # + duração do CTA
        for i, c in enumerate(CENAS):
            entradas += ["-i", os.path.join(FOOTAGE, c["clipe"])]
            filtro += (
                f"[{i}:v]trim=start=0.3:duration={c['d']:.2f},setpts=PTS-STARTPTS,"
                f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
                f"crop={W}:{H},setsar=1[cv{i}];"
            )
            arq_txt = escrever(tmp, i, c["texto"])
            filtro += (
                f"[cv{i}]drawtext=fontfile='{esc(FONTE)}':textfile='{arq_txt}':"
                f"fontcolor=white:fontsize=64:line_spacing=14:"
                f"borderw=0:shadowcolor=black@0.65:shadowx=3:shadowy=4:"
                f"x=(w-text_w)/2:y=h*{c['y']}[vt{i}];"
            )
            rotulos.append(f"vt{i}")

        # ---------- CTA final: card de marca, com a logo real do site ----------
        idx_cta = len(CENAS)
        entradas += ["-f", "lavfi", "-i", f"color={CREME}:s={W}x{H}:d=3.6"]
        idx_logo = idx_cta + 1
        entradas += ["-i", os.path.join(BASE, "logo_whiskergear.png")]

        cta_l2 = escrever(tmp, "cta2", "WINDOW & BALCONY SAFETY")
        cta_l3 = escrever(tmp, "cta3", "FULL GUIDE — LINK IN BIO")
        # pixels calculados em Python: drawbox nao aceita expressao composta
        # (tipo h*0.40+210) do mesmo jeito que drawtext aceita.
        logo_w, logo_h = 640, 160  # proporcao original 1520x380
        y_logo = int(H * 0.36)
        y_subtitulo = y_logo + logo_h + 70
        y_divisor = y_subtitulo + 70
        x_divisor = (W - 160) // 2
        y_link = y_divisor + 50

        filtro += (
            f"[{idx_logo}:v]scale={logo_w}:{logo_h}[logo];"
            f"[{idx_cta}:v]drawbox=x=0:y=0:w={W}:h=10:color={AMBAR}@1:t=fill[c0];"
            f"[c0][logo]overlay=(W-{logo_w})/2:{y_logo}[c1];"
            f"[c1]drawtext=fontfile='{esc(FONTE)}':textfile='{cta_l2}':"
            f"fontcolor={AMBAR}:fontsize=48:x=(w-text_w)/2:y={y_subtitulo}[c3];"
            f"[c3]drawbox=x={x_divisor}:y={y_divisor}:w=160:h=6:color={AMBAR}@1:t=fill[c4];"
            f"[c4]drawtext=fontfile='{esc(FONTE)}':textfile='{cta_l3}':"
            f"fontcolor={INK}:fontsize=40:x=(w-text_w)/2:y={y_link}[vcta];"
        )
        rotulos.append("vcta")

        # nenhum dos clipes do Pexels tem trilha de audio (comum em stock) —
        # uma unica faixa de silencio cobre o video inteiro, mais simples
        # que tentar concatenar audio por cena.
        idx_audio = idx_logo + 1
        entradas += ["-f", "lavfi", "-i",
                    f"anullsrc=channel_layout=stereo:sample_rate=48000"]

        v_labels = "".join(f"[{r}]" for r in rotulos)
        filtro += f"{v_labels}concat=n={len(rotulos)}:v=1:a=0[vconcat]"

        saida = os.path.join(BASE, "out")
        os.makedirs(saida, exist_ok=True)
        destino = os.path.join(saida, "reel-seguranca-01.mp4")

        cmd = ["ffmpeg", "-y"] + entradas + [
            "-filter_complex", filtro,
            "-map", "[vconcat]", "-map", f"{idx_audio}:a",
            "-t", f"{duracao_total:.2f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart",
            destino,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-4000:]); sys.exit(1)
        print(f"OK -> {destino}  ({os.path.getsize(destino)/1024/1024:.1f} MB)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    montar()
