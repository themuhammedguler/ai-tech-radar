<h1 align="center">AI & Tech Daily Radar</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?logo=github-actions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Tests-29%20Passed%20(Pytest)-brightgreen?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Sources-4%20Channels%20%7C%2025%20Trends-orange" alt="4 Channels">
  <img src="https://img.shields.io/badge/AI%20Summary-Gemini%20Flash%20TL%3BDR-8E44AD?logo=google&logoColor=white" alt="Gemini Flash">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
</p>

<p align="center">
  <strong>Otonom ETL Veri Hattı &bull; 25 Maddelik Kapsamlı Teknoloji, Yazılım ve Yapay Zeka Trend Radarı</strong><br>
  <em>HackerNews (10), GitHub Trending (5), Hugging Face (5) ve ArXiv (5) üzerindeki sinyalleri yakalar, gürültüyü akıllı NLP kurallarıyla eler ve Gemini Flash ile 3 maddelik yönetici brifingi üretir.</em>
</p>

---

<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `2026-11-27`

> 📊 **Bugünün Özeti:** 25 teknoloji trendi (10 HackerNews + 5 GitHub + 5 Hugging Face + 5 ArXiv) tarandı.  
> 📑 **Tam Rapor:** [Günün 25 Maddelik Raporunu Görüntüle (`reports/2026-11-27.md`)](reports/2026-11-27.md)

#### 🧠 Günün Yapay Zeka Özeti (Executive Briefing)
- 🌐 **Sektör & Büyük Olaylar:** Google'ın Model Context Protocol (MCP) hamlesi ve yapay zeka ajanlarının güvenlik sınırları tartışılırken; ABD Hava Kuvvetleri bulut platformunun hacklenmesi, yapay zekanın yol açtığı siber güvenlik açıklarına dair endişeleri kritik bir seviyeye taşıdı.
- 🛠️ **Yazılım & Açık Kaynak:** Geliştirici ekosisteminde özellikle Rust odaklı sistem programlama projeleri öne çıkarken; yapay zekanın kendi kendine barındırma (self-hosting) süreçlerini yeniden eğlenceli ve erişilebilir kılması yazılım geliştirme pratiklerini dönüştürüyor.
- 🔬 **Yapay Zeka & Araştırma:** Bilgisayar kullanabilen genel amaçlı ajanların uzun soluklu iş akışlarındaki performansını ölçen yeni kıyaslama (benchmark) çalışmalarının yanı sıra, Transformer mimarilerindeki kararsızlıkları gidermeye yönelik DeltaNet ve döngüsel (Mixture-of-Loops) hibrit yaklaşımlar popülerlik kazanıyor.

#### 🔥 HackerNews Öne Çıkanlar
| Kategori | Başlık | Puan | Yorum | HN Linki |
|:--------:|--------|:----:|:-----:|:--------:|
| `🤖 AI / ML` | [AI made self-hosting fun again](https://janlukas.blog/posts/ai-self-hosting) | ⭐ 925 | 💬 447 | [Tartışma](https://news.ycombinator.com/item?id=50660180) |
| `🤖 AI / ML` | [Google Will Make AI Agents Use Its MCP Servers. The Gmail One Can't Send Email](https://techstackups.com/articles/google-workspace-ai-agents-mcp/) | ⭐ 384 | 💬 318 | [Tartışma](https://news.ycombinator.com/item?id=50653477) |
| `💻 Yazılım & Geliştirme` | [YouTube Ad Punisher – Auto-reloads YouTube pages when an ad plays](https://github.com/antonpictures/youtube-punisher) | ⭐ 480 | 💬 566 | [Tartışma](https://news.ycombinator.com/item?id=50657530) |
| `🤖 AI / ML` | [The group chat where your AI talks behind your back](https://construct22.com/) | ⭐ 514 | 💬 225 | [Tartışma](https://news.ycombinator.com/item?id=50663595) |
| `🤖 AI / ML` | [AMD-specific fork of llama.cpp](https://devnull.land/amd-specific-llama-cpp) | ⭐ 411 | 💬 101 | [Tartışma](https://news.ycombinator.com/item?id=50657265) |

#### ⭐ GitHub Trending Açık Kaynak Projeler
| Proje | Dil | Yıldız | Açıklama |
|-------|:---:|:------:|----------|
| [**Marvisak/VIctory**](https://github.com/Marvisak/VIctory) | `Rust` | ⭐ 13,686 | An attempt at running GTA VI on PC |
| [**erkamyaman/rust-anything**](https://github.com/erkamyaman/rust-anything) | `Rust` | ⭐ 10,649 | Rewrite your app in Rust, piece by piece, checked against the original at every ... |
| [**xcl-dev/xcl**](https://github.com/xcl-dev/xcl) | `Rust` | ⭐ 8,692 | Xbox Series compatibility layer for Windows - runs console game code natively, r... |

#### 🔬 Öne Çıkan AI & Model Araştırmaları (Hugging Face & ArXiv)
- 🤗 **[Stable Gated DeltaNet-2: Understanding and Mitigating Recurrent State Instability](https://huggingface.co/papers/2611.34051)** `HuggingFace` *(🔺 124 oy · Xichong Zhang, Xixuan Hao vb.)*
  Linear attention offers an efficient solution for long-sequence modeling via linear complexity and fixed-size recurrent states. Gated DeltaNet-2 (GDN-2) introduces independent channel-wise control over erasure and writing, enhancing state-update expressiveness and in-context retrieval, yet it suffers from training failures during long-context training.

- 🤗 **[OS-Omni: Benchmarking Generalist Computer-Using Agents on Long-Horizon Workflows Across Platforms](https://huggingface.co/papers/2611.34232)** `HuggingFace` *(🔺 98 oy · Hui Shen, Yunta Hsieh vb.)*
  Computer-using agents are increasingly expected to complete realistic user goals rather than isolated GUI actions. However, existing benchmarks typically isolate web, mobile, or desktop environments, leaving it unclear whether a single generalist agent can execute long-horizon workflows that span multiple operating systems and persistent application states.

- 🤖 **[Spectrum Adaptation of AI-Native Autoencoder Communications with Transfer Learning](https://arxiv.org/abs/2611.34942v1)** `cs.NI` *(Yazarlar: Yalin E. Sagduyu, Tugba Erpek)*
  *📅 Yayın: 2026-11-25* — End-to-end physical-layer learning replaces separate modulation, coding, and detection operations with an autoencoder (AE) that consists of a jointly trained encoder-decoder pair at the transmitter and the receiver. This paper studies AI-native communications with AEs and quantifies the sensitivity to training-test mismatch in channel models.

- 🤖 **[Tokenisation is not in APX](https://arxiv.org/abs/2611.34938v1)** `cs.CL` *(Yazarlar: Violeta Kastreva, Philip Whittington, Dennis Komm vb.)*
  *📅 Yayın: 2026-11-25* — In this paper, we prove that, unless P=NP, no polynomial-time algorithm can find a tokeniser whose objective is within any constant factor of the optimum, meaning that tokenisation is not in the APX complexity class. We prove this for direct and bottom-up tokenisation, under both a compression or unigram log-likelihood objectives, and for binary or larger alphabets.

#### 🗄️ Son 7 Günün Rapor Arşivi
- [📅 2026-11-27 Raporu](reports/2026-11-27.md)
- [📅 2026-11-26 Raporu](reports/2026-11-26.md)
- [📅 2026-11-25 Raporu](reports/2026-11-25.md)
- [📅 2026-11-24 Raporu](reports/2026-11-24.md)
- [📅 2026-11-22 Raporu](reports/2026-11-22.md)
- [📅 2026-11-21 Raporu](reports/2026-11-21.md)
- [📅 2026-11-20 Raporu](reports/2026-11-20.md)
<!-- LATEST_REPORT_END -->

---

## 🏗️ Üretim Seviyesi Modüler Mimari

Proje, tek dosyalık prototip yaklaşımından çıkarılıp **Clean Architecture** ve **SOLID** prensiplerine uygun olarak modüler paketlere ayrılmıştır:

```
src/
├── config.py                 # Merkezi ayarlar, zaman aşımları, API uçları ve kategoriler
├── models.py                 # Tip güvenliği ve doğrulama modelleri (TrendItem, GithubRepoItem, ArxivPaper vb.)
├── logging_config.py         # Yapılandırılmış, renkli ve seviyeli logging altyapısı
├── pipeline.py               # 4 kaynak ve AI sentezleyiciyi yöneten ana orkestratör
├── fetch_trends.py           # CLI ve GitHub Actions giriş noktası
├── collectors/               # Veri Toplayıcılar (Resilient Session + Pooling)
│   ├── base.py               # Temel toplayıcı, retry stratejisi ve zaman aşımları
│   ├── hackernews.py         # Algolia API üzerinden 50 aday HN haberi toplayıcı
│   ├── github_trending.py    # GitHub Search API ile son günlerin en popüler açık kaynak projeleri
│   ├── huggingface.py        # Hugging Face Daily Papers ile topluluğun en çok oyladığı AI makaleleri
│   └── arxiv.py              # Güvenli HTTPS üzerinden ArXiv Atom XML toplayıcı
├── processors/               # Veri İşleme & Yapay Zeka Sentezi
│   ├── content_filter.py     # Negatif filtre (ölüm/ilan eleme) ve kategori skor motoru
│   ├── text_summarizer.py    # Anlam bütünlüğünü koruyan cümle ayıklayıcı
│   └── ai_summarizer.py      # Google Gemini Flash ile 3 tematik maddelik Türkçe yönetici özeti
└── generators/               # Çıktı Üreticileri
    ├── report_generator.py   # 25 maddelik zengin reports/YYYY-MM-DD.md üretim motoru
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
