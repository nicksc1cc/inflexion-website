Rebuild from the repository root:

```bash
cd tools/pathways/s1 && python3 compile.py && cd .. && python3 fit.py && python3 build.py
cp site/pathways/index.html ../../pathways/index.html
cp site/pathways/pathways-data.json pathways-data.json
rm -rf site pathways.html
python3 copy_check.py ../../pathways/index.html
```

`build.py` generates a temporary `site/pathways/` output. The final site page lives at `../../pathways/index.html` and is copied from that generated output after the build.
