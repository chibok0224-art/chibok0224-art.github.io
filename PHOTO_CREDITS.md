# Category photos

Files in `static/img/photo/` (960x540 WebP, cropped from the originals). All are from Unsplash under the
Unsplash License (free for commercial use, no attribution required). Checked as "Free", not Unsplash+, on 2026-10-02. Six were replaced the same day after review (brighter, clearer subjects).

| Category | Photo | Photographer |
|---|---|---|
| graphics-design | https://unsplash.com/photos/gcHFXsdcmJE | Kelly Sikkema |
| programming-tech | https://unsplash.com/photos/f77Bh3inUpE | Arnold Francisca |
| online-marketing | https://unsplash.com/photos/SB0WARG16HI | Diggity Marketing |
| video-animation | https://unsplash.com/photos/u4bvBOOpZB4 | Sanjeev Nagaraj |
| writing-translation | https://unsplash.com/photos/FHnnjk1Yj7Y | Nick Morrison |
| music-audio | https://unsplash.com/photos/XJK8gdWpxWk | Lewis Guapo |
| business | https://unsplash.com/photos/QckxruozjRg | Annie Spratt |
| finance | https://unsplash.com/photos/9PwLeZA-RGc | Jakub Żerdzicki |
| ai-services | https://unsplash.com/photos/_0iV9LmPDn0 | Steve A Johnson |
| lifestyle | https://unsplash.com/photos/IeTLKtzbLNo | Chase Yi |
| consulting-services | https://unsplash.com/photos/JaoVGh5aJ3E | Amy Hirschi |
| data | https://unsplash.com/photos/JKUTrJ4vK00 | Luke Chesser |
| photography | https://unsplash.com/photos/WxM465oM4j4 | Reinhart Julian |

To replace a photo: download `https://images.unsplash.com/<photo-file>?w=960&h=540&fit=crop&crop=entropy&fm=webp&q=70`
to `static/img/photo/<category>.webp` and update this table. Without a photo the build falls back to `static/img/cat/<category>.svg`.
