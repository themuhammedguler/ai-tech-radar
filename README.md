# 📡 AI & Tech Daily Radar

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?logo=github-actions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Tests-23%20Passed%20(Pytest)-brightgreen?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Architecture-Modular%20SOLID-purple" alt="Modular SOLID">
  <img src="https://img.shields.io/badge/Security-Enforced%20HTTPS-success?logo=letsencrypt&logoColor=white" alt="HTTPS Enforced">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
</p>

> **AI & Tech Daily Radar**, her gün GitHub Actions üzerinde otonom çalışan, kurumsal seviyede hata toleransına, modüler mimariye ve otomatik test güvencesine sahip bir **Yapay Zeka ve Teknoloji Veri Hattıdır (ETL Pipeline)**.
> HackerNews ve ArXiv (`cs.AI`, `cs.LG`, `cs.CL`) üzerindeki sinyalleri yakalar, gürültüyü akıllı NLP kurallarıyla eler ve şeffaf biçimde raporlar.

---

<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `2026-11-12`

> 📊 **Bugünün Özeti:** 10 yüksek nitelikli teknoloji trendi ve 5 ArXiv AI/ML akademik makalesi tarandı.  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/2026-11-12.md`)](reports/2026-11-12.md)

#### 🔥 HackerNews Öne Çıkanlar
| Kategori | Başlık | Puan | Yorum | HN Linki |
|:--------:|--------|:----:|:-----:|:--------:|
| `🤖 AI / ML` | [Nvidia is preparing to oust Jensen Huang](https://www.wsj.com/business/nvidia-is-preparing-to-oust-nvidia-ceo-jensen-huang-30f421ad) | ⭐ 1170 | 💬 1562 | [Tartışma](https://news.ycombinator.com/item?id=50459703) |
| `💻 Yazılım & Geliştirme` | [AWS emulator](https://github.com/aws/aws-emulator) | ⭐ 904 | 💬 250 | [Tartışma](https://news.ycombinator.com/item?id=50456631) |
| `🤖 AI / ML` | [United Airlines bans AI agents from booking flights on behalf of travelers](https://www.cbsnews.com/news/united-airlines-bans-ai-agents-booking-flights/) | ⭐ 607 | 💬 631 | [Tartışma](https://news.ycombinator.com/item?id=50458900) |
| `🤖 AI / ML` | [Gemini Decisions API](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/) | ⭐ 497 | 💬 148 | [Tartışma](https://news.ycombinator.com/item?id=50456791) |
| `🤖 AI / ML` | [NVIDIA Announces CEO Transition](https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition) | ⭐ 509 | 💬 367 | [Tartışma](https://news.ycombinator.com/item?id=50467087) |

#### 🤖 ArXiv AI/ML Öne Çıkan Araştırmalar
- 📄 **[Medical Image Segmentation: Foundation Model Adaptation versus Task-Specific Training](https://arxiv.org/abs/2611.14519v1)** `cs.CV` *(Yazarlar: Emre Kutlusan, Yongmin Li)*
  *📅 Yayın: 2026-11-10* — Foundation models pretrained on large natural-image collections are increasingly adapted for medical image segmentation, in the expectation that they will replace models trained for each task.

- 📄 **[Toward Foundation Detection Models via Example-Based Grounding in EM-DETR](https://arxiv.org/abs/2611.14518v1)** `cs.CV` *(Yazarlar: Sheethal Bhat, Bogdan Georgescu, Awais Mansoor vb.)*
  *📅 Yayın: 2026-11-10* — DeepLearning (DL)-based Computer-Aided Diagnostic (CAD) systems have shown great promise in supporting clinicians, but their performance heavily depends on the availability of large, well-annotated datasets.

- 📄 **[TorchCurves: Differentiable Parametric Curves](https://arxiv.org/abs/2611.14516v1)** `cs.LG` *(Yazarlar: Alex Shtoff)*
  *📅 Yayın: 2026-11-10* — We present TorchCurves, a PyTorch library that treats vector-valued parametric curves as learnable primitives. Its central operation maps batches of scalar inputs to points on curves represented in B-spline or Legendre polynomial bases, with differentiation through both inputs and coefficients.

#### 🗄️ Son 7 Günün Rapor Arşivi
- [📅 2026-11-12 Raporu](reports/2026-11-12.md)
- [📅 2026-11-11 Raporu](reports/2026-11-11.md)
- [📅 2026-11-10 Raporu](reports/2026-11-10.md)
- [📅 2026-11-08 Raporu](reports/2026-11-08.md)
- [📅 2026-11-07 Raporu](reports/2026-11-07.md)
- [📅 2026-11-06 Raporu](reports/2026-11-06.md)
- [📅 2026-11-05 Raporu](reports/2026-11-05.md)
<!-- LATEST_REPORT_END -->

---

## 🏗️ Üretim Seviyesi Modüler Mimari

Proje, tek dosyalık prototip yaklaşımından çıkarılıp **Clean Architecture** ve **SOLID** prensiplerine uygun olarak modüler paketlere ayrılmıştır:

```
src/
├── config.py                 # Merkezi ayarlar, zaman aşımları, filtre kuralları ve kategoriler
├── models.py                 # Immutability ve doğrulama garantili veri modelleri (TrendItem, ArxivPaper)
├── logging_config.py         # Yapılandırılmış, renkli ve standart logging altyapısı
├── pipeline.py               # Uçtan uca veri akışı orkestratörü ve kritik hata denetleyicisi
├── fetch_trends.py           # CLI ve GitHub Actions giriş noktası
├── collectors/               # Veri Toplayıcılar (Abstract Base Class + Connection Pooling)
│   ├── base.py               # Resilient HTTP Session, exponential backoff retries, timeouts
│   ├── hackernews.py         # Algolia API üzerinden 50 aday toplayıcı
│   └── arxiv.py              # Güvenli HTTPS üzerinden ArXiv Atom XML toplayıcı
├── processors/               # Veri İşleme & Rafine Etme
│   ├── content_filter.py     # Akıllı negatif filtre (ölüm/ilan eleme) ve teknoloji önceliklendirme
│   └── text_summarizer.py    # Anlam bütünlüğünü koruyan akıllı cümle çıkarıcı
└── generators/               # Çıktı Üreticileri
    ├── report_generator.py   # reports/YYYY-MM-DD.md üretim motoru
    └── readme_updater.py     # README.md dinamik blok senkronizasyonu
```

---

## 🛡️ Güvenilirlik ve Hata Toleransı İlkeleri

Sistem, harici API arızalarını ve veri kirliliğini engellemek için kurumsal standartlarda geliştirilmiştir:

1. **Uçtan Uca HTTPS Güvenliği:**
   - ArXiv API bağlantısı zorunlu olarak **`https://export.arxiv.org`** protokolüyle şifreli çalışır.
2. **Kritik Veri Doğrulaması:**
   - API başarısızlıklarının gizlenmesi engellenmiştir. Eğer veri akışı tamamen kesilirse pipeline sessizce başarılı sayılmaz (`exit 1` ile GitHub Actions uyarılır), boş veya bozuk raporların commitlenmesi önlenir.
3. **Şeffaf Tarih ve Fallback Yönetimi:**
   - ArXiv hafta sonu yeni makale yayınlamadığında, geçmiş makaleler asla "günün makalesi" gibi yanıltıcı gösterilmez. Gerçek yayınlanma tarihleri (`atom:published`) ve `(Referans Arşiv)` etiketi açıkça belirtilir.
4. **Dayanıklı HTTP İstekleri:**
   - `urllib3.util.retry.Retry` stratejisi ile HTTP 429, 500, 502, 503, 504 durumlarında exponential backoff ile 3 defa otomatik yeniden denenir.
   - Ayrı bağlantı (`5s`) ve okuma (`25s`) zaman aşımları uygulanır.
5. **Akıllı İçerik Süzgeci:**
   - Vefat haberleri, magazin, iş ilanları ve saf tıp yazıları filtrelenirken, sağlık alanındaki gerçek AI çalışmaları ("CNN outperforms LLMs for diagnosis") bağlam analizcisi ile korunur.

---

## 🧪 Test Süreci

Proje, **%100 kapsamlı birim ve entegrasyon test paketine** (`pytest`) sahiptir:

```bash
# Geliştirme bağımlılıklarını kurun
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Tüm testleri çalıştırın
pytest -v
```

CI/CD hattında (`daily_radar.yml`), testler başarıyla geçmeden veri hattı çalıştırılmaz.

---

## 🚀 Yerel Çalıştırma

```bash
# 1. Depoyu klonlayın
git clone https://github.com/themuhammedguler/ai-tech-radar.git
cd ai-tech-radar

# 2. Pipeline'ı çalıştırın
python src/fetch_trends.py
```

---

## 📜 Lisans

Bu proje [MIT](LICENSE) lisansı ile lisanslanmıştır.
