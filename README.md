# 📡 AI & Tech Daily Radar

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?logo=github-actions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Data_Sources-HackerNews%20%7C%20ArXiv-orange" alt="Data Sources">
  <img src="https://img.shields.io/badge/Pipeline-Autonomous_ETL-success" alt="ETL Pipeline">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
</p>

> **AI & Tech Daily Radar**, her gün GitHub Actions üzerinde otonom olarak çalışan; HackerNews üzerindeki en sıcak teknoloji gelişmelerini ve ArXiv üzerindeki en yeni Yapay Zeka / Makine Öğrenimi (AI & ML) araştırma makalelerini toplayıp derleyen modern bir veri hattıdır (data pipeline).

---

<!-- LATEST_REPORT_START -->
### ⚡ Son Güncelleme: `2026-11-01`

> 📊 **Bugünün Özeti:** 10 HackerNews teknoloji trendi ve 5 ArXiv AI/ML akademik makalesi tarandı.  
> 📑 **Tam Rapor:** [Günün Raporunu Görüntüle (`reports/2026-11-01.md`)](reports/2026-11-01.md)

#### 🔥 HackerNews Öne Çıkanlar
| Başlık | Puan | Yorum | HN Linki |
|--------|:----:|:-----:|:--------:|
| [HackerTube: YouTube built from videos recommended by HN](https://karpathy.bearblog.dev/hacker-tube/) | ⭐ 1471 | 💬 397 | [Tartışma](https://news.ycombinator.com/item?id=50319510) |
| [TCP Use-After-Free: CVE-2026-98432 / CVSS 9.8](https://atlasum.net/blog/cve-2026-98432-linux-ipv4-tcp-uaf) | ⭐ 548 | 💬 250 | [Tartışma](https://news.ycombinator.com/item?id=50319143) |
| [An Italian farmer found some unknown seeds in his attic and planted them](https://www.smithsonianmag.com/science-nature/italian-farmer-found-unknown-seeds-attic-with-nothing-lose-planted-them-result-biblical-180989644/) | ⭐ 512 | 💬 158 | [Tartışma](https://news.ycombinator.com/item?id=50320963) |
| [Do the math: How we took over ChatGPT accounts](https://www.parameter.ai/labs/we-found-a-gap-at-openai) | ⭐ 344 | 💬 168 | [Tartışma](https://news.ycombinator.com/item?id=50314699) |
| [Jepsen: ParticleDB 1.1.4](https://jepsen.io/analyses/particledb-1.1.4) | ⭐ 282 | 💬 161 | [Tartışma](https://news.ycombinator.com/item?id=50316100) |

#### 🤖 ArXiv AI/ML Öne Çıkan Araştırmalar
- 📄 **[Propose-Filter-Release: Scaling Noise to Typical Sensitivity via Private Filtering](http://arxiv.org/abs/2610.40654v1)**
  *An estimator can be accurate and stable on typical data, yet sensitive to a few possible records. Differentially private mechanisms commonly scale their noise to the worst-case influence of a single r...*

- 📄 **[Rethinking Neural Thickets Without Weight Perturbations](http://arxiv.org/abs/2610.40649v1)**
  *The Neural Thickets hypothesis posits that pretrained language models lie in dense neighborhoods of task-specific experts in weight space, which random Gaussian perturbations can uncover. We reproduce...*

- 📄 **[Read, Allocate, Route: Role-Coupled Tokenization for Pixel-Space Generative Transformers](http://arxiv.org/abs/2610.40647v1)**
  *Pixel-space generative Transformers typically use one token per image patch, so capturing finer detail requires more tokens and makes global attention increasingly expensive. We observe that finer det...*

#### 🗄️ Son 7 Günün Rapor Arşivi
- [📅 2026-11-01 Raporu](reports/2026-11-01.md)
- [📅 2026-10-31 Raporu](reports/2026-10-31.md)
- [📅 2026-10-30 Raporu](reports/2026-10-30.md)
- [📅 2026-10-29 Raporu](reports/2026-10-29.md)
- [📅 2026-10-28 Raporu](reports/2026-10-28.md)
- [📅 2026-10-27 Raporu](reports/2026-10-27.md)
- [📅 2026-10-26 Raporu](reports/2026-10-26.md)
<!-- LATEST_REPORT_END -->

---

## 🏗️ Mimari ve Nasıl Çalışır?

Bu sistem, harici bir sunucu veya veritabanı ihtiyacı olmadan tamamen **serverless** ve **Git-as-a-Database** yaklaşımıyla çalışacak şekilde tasarlanmıştır:

```mermaid
flowchart LR
    A["⏰ GitHub Actions Cron<br/>(Her gün UTC 06:00)"] --> B["🐍 Python Pipeline<br/>(fetch_trends.py)"]
    B --> C["📰 HackerNews API<br/>(Top 10 Tech News)"]
    B --> D["📚 ArXiv API<br/>(Latest AI/ML Papers)"]
    C --> E["📝 Rapor Üretimi<br/>(reports/YYYY-MM-DD.md)"]
    D --> E
    E --> F["📄 README Güncelleme<br/>(Özet + Son 7 Gün Arşivi)"]
    F --> G["🚀 Git Commit & Push<br/>(Otonom Versiyonlama)"]
```

### ⚙️ Çalışma Aşamaları (ETL)

1. **Extract (Çıkarma):**
   - **HackerNews Algolia API:** Günün en popüler 10 teknoloji trendini (başlık, puan, yorum sayısı, URL) çeker.
   - **ArXiv API:** Bilgisayar Bilimleri / Yapay Zeka (`cs.AI`) ve Makine Öğrenimi (`cs.LG`) kategorilerinde yayımlanan en güncel 5 akademik makaleyi (`ElementTree` XML ayrıştırıcı ile) çeker.

2. **Transform (Dönüştürme):**
   - Alınan ham veriler standart bir Markdown formatına dönüştürülür.
   - Makale özetleri optimize edilir, tablolar ve bağlantılar biçimlendirilir.
   - Son 7 günün arşiv linkleri otomatik tespit edilir.

3. **Load (Yükleme & Dağıtım):**
   - Günün tarihine özel `reports/YYYY-MM-DD.md` dosyası oluşturulur.
   - Ana dizindeki `README.md` dosyasındaki belirlenmiş işaretçiler arasına güncel özet ve arşiv tablosu işlenir.
   - Değişiklikler GitHub Actions botu tarafından depoya geri `commit` ve `push` edilir.

---

## 🚀 Yerel Kurulum ve Çalıştırma

Projeyi yerel makinenizde test etmek isterseniz:

```bash
# 1. Projeyi klonlayın
git clone https://github.com/themuhammedguler/ai-tech-radar.git
cd ai-tech-radar

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Veri hattını çalıştırın
python src/fetch_trends.py
```

Rapor oluşturulduktan sonra `reports/` dizinini ve `README.md` dosyasını inceleyebilirsiniz.

---

## 📜 Lisans

Bu proje [MIT](LICENSE) lisansı ile lisanslanmıştır.
