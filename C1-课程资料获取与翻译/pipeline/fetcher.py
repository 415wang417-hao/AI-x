import os
import sys
import zipfile
import hashlib
import json
import urllib.request
import argparse
from typing import Dict, Any, List

class SourceFetcher:
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.materials_dir = os.path.join(self.base_dir, 'materials')
        self.raw_dir = os.path.join(self.base_dir, 'raw_sources')
        os.makedirs(self.raw_dir, exist_ok=True)

    @staticmethod
    def calculate_sha256(filepath: str) -> str:
        h = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192 * 16):
                h.update(chunk)
        return h.hexdigest().upper()

    def verify_manifest(self, manifest_path: str = None) -> Dict[str, Any]:
        mp = manifest_path or os.path.join(self.base_dir, 'MANIFEST.txt')
        if not os.path.exists(mp):
            return {"status": "SKIPPED", "message": "Manifest file not found"}
        
        results = []
        with open(mp, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2 and len(parts[0]) == 64:
                expected_sha = parts[0].upper()
                rel_path = parts[1]
                full_path = os.path.join(self.base_dir, rel_path)
                if os.path.exists(full_path):
                    actual_sha = self.calculate_sha256(full_path)
                    match = (actual_sha == expected_sha)
                    results.append({
                        "file": rel_path,
                        "match": match,
                        "expected": expected_sha,
                        "actual": actual_sha
                    })
                else:
                    results.append({
                        "file": rel_path,
                        "match": False,
                        "error": "File missing"
                    })
        all_passed = all(r.get('match', False) for r in results)
        return {
            "status": "PASS" if all_passed else "FAIL",
            "checks": results
        }

    def unpack_offline_cache(self, zip_path: str = None, target_dir: str = None) -> str:
        zp = zip_path or os.path.join(self.materials_dir, 'CS146S_offline.zip')
        dest = target_dir or os.path.join(self.raw_dir, 'CS146S_offline')
        if not os.path.exists(zp):
            raise FileNotFoundError(f"Offline zip package not found at: {zp}")

        print(f"[Fetcher] Extracting offline cache from {zp} to {dest}...")
        with zipfile.ZipFile(zp, 'r') as zf:
            zf.extractall(self.raw_dir)
        print(f"[Fetcher] Extraction complete: {dest}")
        return dest

    def fetch_url(self, url: str, output_path: str) -> bool:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CS146S-Course-Pipeline/1.0'}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(content)
            print(f"[Fetcher] Successfully downloaded: {url} -> {output_path}")
            return True
        except Exception as e:
            print(f"[Fetcher] Failed to download {url}: {e}")
            return False

    def run(self, source_path: str = None) -> Dict[str, Any]:
        manifest_res = self.verify_manifest()
        extracted_path = self.unpack_offline_cache(source_path)
        return {
            "manifest_verification": manifest_res,
            "raw_source_dir": extracted_path,
            "status": "SUCCESS"
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Course Material Fetcher & Integrity Verifier")
    parser.add_argument('--verify-only', action='store_true', help="Only verify checksums")
    parser.add_argument('--source', type=str, default=None, help="Custom zip path or source URL")
    args = parser.parse_args()

    fetcher = SourceFetcher()
    if args.verify_only:
        res = fetcher.verify_manifest()
        print(json.dumps(res, indent=2))
    else:
        res = fetcher.run(args.source)
        print("[Fetcher] Status:", res['status'])
