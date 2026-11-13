<h1 align="center">AI & Tech Daily Radar</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?logo=github-actions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Tests-23%20Passed%20(Pytest)-brightgreen?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Architecture-Modular%20SOLID-purple" alt="Modular SOLID">
  <img src="https://img.shields.io/badge/Security-Enforced%20HTTPS-success?logo=letsencrypt&logoColor=white" alt="HTTPS Enforced">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
</p>

<p align="center">
  <strong>Otonom ETL Veri Hattı &bull; Günlük Teknoloji, Yazılım ve Yapay Zeka Trend Radarı</strong><br>
  <em>HackerNews ve ArXiv (cs.AI, cs.LG, cs.CL) üzerindeki sinyalleri yakalar, gürültüyü akıllı NLP kurallarıyla eler ve şeffaf biçimde raporlar.</em>
</p>

---

<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `2026-11-13`

> 📊 **Bugünün Özeti:** 10 yüksek nitelikli teknoloji trendi ve 5 ArXiv AI/ML akademik makalesi tarandı.  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/2026-11-13.md`)](reports/2026-11-13.md)

#### 🔥 HackerNews Öne Çıkanlar
| Kategori | Başlık | Puan | Yorum | HN Linki |
|:--------:|--------|:----:|:-----:|:--------:|
| `🤖 AI / ML` | [Anthropic IPO](https://ipo.anthropic.com/us/) | ⭐ 897 | 💬 851 | [Tartışma](https://news.ycombinator.com/item?id=50465829) |
| `💻 Yazılım & Geliştirme` | [Rust 1.100](https://blog.rust-lang.org/2026/11/12/Rust-1.100.0/) | ⭐ 602 | 💬 229 | [Tartışma](https://news.ycombinator.com/item?id=50472038) |
| `🤖 AI / ML` | [Gemini 4 Hydrogen](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) | ⭐ 509 | 💬 324 | [Tartışma](https://news.ycombinator.com/item?id=50471431) |
| `💻 Yazılım & Geliştirme` | [Show HN: My $300 embroidery machine needed a subscription, so I built my own app](https://github.com/simpsoka/zigzag) | ⭐ 463 | 💬 171 | [Tartışma](https://news.ycombinator.com/item?id=50470488) |
| `🤖 AI / ML` | [Nvidia employees petition to bring back Jensen Huang](https://www.wired.com/story/nvidia-employees-petition-for-jensen-huangs-return/) | ⭐ 404 | 💬 306 | [Tartışma](https://news.ycombinator.com/item?id=50477231) |

#### 🤖 ArXiv AI/ML Öne Çıkan Araştırmalar
- 📄 **[Unbundling Multimodal Vision Encoding](https://arxiv.org/abs/2611.17334v1)** `cs.CV` *(Yazarlar: Ellis Brown, Chris Hoang, Shengyi Qian vb.)*
  *📅 Yayın: 2026-11-12* — How multimodal language models should encode visual input remains up for debate. Most models use a pretrained vision encoder, while some recent recipes train the encoder from scratch with the language model or remove it entirely.

- 📄 **[ArchSpace: Recording, Reviewing, and Referencing LLM Architecture Research](https://arxiv.org/abs/2611.17332v1)** `cs.CL` *(Yazarlar: Jie Wang, Tong Zhu, JiaHao Kuang vb.)*
  *📅 Yayın: 2026-11-12* — Model architecture shapes the scaling behavior, training efficiency, and inference cost of LLMs, making it a central focus of both industry and academia. In industry, teams such as those behind DeepSeek, Qwen, and Kimi routinely introduce architectural innovations, yet public reports rarely document which ideas succeeded, which were abandoned, and why.

- 📄 **[Internalizing Investment Mandates: A Neurosymbolic RL Approach to Portfolio Allocation](https://arxiv.org/abs/2611.17329v1)** `cs.LG` *(Yazarlar: Zeynep Yıldız, Satchit Chatterji, Ercan Atam vb.)*
  *📅 Yayın: 2026-11-12* — Institutional portfolios operate under investment policy statements that specify asset allocation constraints, often conditioned on market regime information. Deep reinforcement learning has been shown to optimize financial performance but typically does not enforce rule compliance, making it unsuitable for real-world deployment.

#### 🗄️ Son 7 Günün Rapor Arşivi
- [📅 2026-11-13 Raporu](reports/2026-11-13.md)
- [📅 2026-11-12 Raporu](reports/2026-11-12.md)
- [📅 2026-11-11 Raporu](reports/2026-11-11.md)
- [📅 2026-11-10 Raporu](reports/2026-11-10.md)
- [📅 2026-11-08 Raporu](reports/2026-11-08.md)
- [📅 2026-11-07 Raporu](reports/2026-11-07.md)
- [📅 2026-11-06 Raporu](reports/2026-11-06.md)
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
