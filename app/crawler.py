# Placeholder for app/crawler.py
import os, httpx, time
DEFAULT_MAX_PAGES = 50
DEFAULT_MAX_DEPTH = 2


class SimpleCrawler:
    def __init__(self, base_url: str, out_dir: str, max_pages: int = DEFAULT_MAX_PAGES, max_depth: int = DEFAULT_MAX_DEPTH):
        self.base_url = base_url.rstrip('/') + '/'
        self.allowed_netloc = urlparse(self.base_url).netloc
        self.out_dir = Path(out_dir)
        self.visited = set()
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.client = httpx.Client(timeout=20.0, follow_redirects=True)


    def in_domain(self, url: str) -> bool:
        return urlparse(url).netloc == self.allowed_netloc


    def fetch(self, url: str) -> str:
        r = self.client.get(url)
        r.raise_for_status()
        return r.text


    def save_doc(self, url: str, html: str):
        doc = Document(html)
        title = doc.short_title() or url
        text_html = doc.summary(html_partial=True)
        # Save as HTML snapshot
        fn = safe_filename(title) + '.html'
        path = self.out_dir / fn
        path.write_text(text_html, encoding='utf-8')
        return str(path)


    def crawl(self):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        queue = [(self.base_url, 0)]
        saved = []
        while queue and len(self.visited) < self.max_pages:
            url, depth = queue.pop(0)
            if url in self.visited or depth > self.max_depth: continue
            self.visited.add(url)
            try:
                html = self.fetch(url)
            except Exception:
                continue
            saved.append(self.save_doc(url, html))
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', href=True):
                nxt = urljoin(url, a['href'])
                if self.in_domain(nxt):
                    queue.append((nxt, depth+1))
        return saved


if __name__ == "__main__":
    base = os.environ.get("ARC_BASE_URL", "https://example.org/")
    out = os.environ.get("DATA_DIR", "./data")
    crawler = SimpleCrawler(base, out)
    saved = crawler.crawl()
    print({"saved": len(saved)})