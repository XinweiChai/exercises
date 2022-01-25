for f in *.pdf; do
  pdftk "$f" output "tmp-$f" uncompress
  sed -i "s/1 0 0 rg/0 0 0 rg/g" "tmp-$f"
  sed -i "s/1 0 0 RG/0 0 0 RG/g" "tmp-$f"
  pdftk "tmp-$f" output "filled-$f" compress
  rm "tmp-$f"
done
