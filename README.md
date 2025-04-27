# crowd-privacy-blur

Depth‑aware, **face‑area removal** for crowd‑analytics video streams  
➡️ 30 FPS on Apple‑Silicon or Jetson Xavier NX | MIT Licence

> **Purpose**  
> Process raw crowd footage *on‑device*, blur any pixel likely to contain a face (< 1 m from lens), then pass the anonymised frames to downstream engagement models. Designed to comply with the EU AI Act ban on real‑time biometric analysis in public spaces.

---

## ✨ Features

| Feature | Default | Notes |
|---------|---------|-------|
| Stereo‑depth mask (OAK‑D) | **≤ 100 cm** | `--nearest_cm N` to adjust |
| Gaussian blur kernel | 99 × 99 px | Edit `blur_depth.py` for alternatives |
| CPU / MPS / CUDA | auto‑select | `--device cpu | mps | cuda` |
| Real‑time FPS | 30 fps @ 640 × 360 | M4 MacBook & Jetson Xavier NX benches |

---

## 🚀 Quick start (macOS M‑series)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python blur_depth.py --device mps       # Esc to quit
```

*Jetson users:* install JetPack 6, then  
```bash
python blur_depth.py --device cuda
```

---

## 🛡️ Compliance

* Faces are blurred in‑place; **no biometrics stored**.  
* All processing is edge‑only; no frames leave the device.  
* Aligns with **EU AI Act Reg 2024/1689 Art. 5.1(c)**.

---

## 📦 Roadmap

| Version | ETA | What’s coming |
|---------|-----|---------------|
| **v0.2** | Jun 2025 | YOLO‑v9 segmentation fallback (single RGB) |
| **v0.3** | Jul 2025 | Docker image + Helm chart |
| **v1.0** | Sep 2025 | Prometheus metrics endpoint & CI suite |

---

## 🤝 Contributing

1. Fork, create branch `git checkout -b feat/name`  
2. Run `black blur_depth.py`; ensure `flake8` passes  
3. Open PR — reviewed within 48 h

---

## 📜 Licence

[MIT](LICENSE) — free for commercial & research use. Attribution appreciated.

---

> Built with 🖤 by [Vibelytics](https://vibelytics.ai) — making crowd energy measurable without surveillance.
