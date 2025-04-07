import json

def generate_shl_catalog_urls(start=0, step=12, max_pages=10):
    urls = []
    for i in range(max_pages):
        offset = start + i * step
        url = f"https://www.shl.com/solutions/products/product-catalog/?start={offset}&type=2&type=1"
        urls.append(url)
    return urls

if __name__ == "__main__":
    # Change max_pages if more pages are added
    catalog_urls = generate_shl_catalog_urls(max_pages=32)

    with open("app/data/Individual_Test_catalog_pages_catalog_pages.json", "w") as f:
        json.dump(catalog_urls, f, indent=2)

    print(f"✅ Saved {len(catalog_urls)} URLs to app/data/Individual_Test_catalog_pages.json")