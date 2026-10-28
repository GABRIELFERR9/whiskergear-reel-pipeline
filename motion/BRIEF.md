---
workflow: general-video
flow: automation
storyboard: no
message: "Preserve the science-backed pet health explainer while removing Gemini Notebook branding and closing with WhiskerGear"
destination: instagram-reels
aspect: 1080x1920
language: en
audience: pet owners
length: 64.83s
angle: source-preserving-edit
---

## Intent

Create one polished vertical WhiskerGear reel from the supplied pet-health explainer. Keep the original English narration, baked captions, illustrations, ordering, and factual content intact. Remove Gemini Notebook branding without inventing new claims.

## Assets

- `C:\Users\CBRO\Downloads\What_Science_Says_About_Pet_Health_Products.mp4` — source picture and audio; editorial content runs through 61.65 s.
- `..\logo_whiskergear.png` — existing official WhiskerGear mark for the replacement closing card.

## Customizations

- Remove the persistent bottom-right Gemini Notebook watermark with a minimal bottom crop and vertical reframe.
- Replace the source's full-screen Gemini Notebook outro with a restrained WhiskerGear logo reveal occupying the same final time window.
- Preserve the source audio; the original narration ends at 61.626 s and the closing hold is intentionally silent.

## Notes

- Autonomous one-shot build, inferred from the direct build instruction; no storyboard review pause.
- Preserve the user's existing modified `out\reel-seguranca-01.mp4`; write a new artifact instead.
- Final cloud delivery: copy the validated MP4 to the installed Google Drive `blog` folder as `PETHOJE.mp4`.
