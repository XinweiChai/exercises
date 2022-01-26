for f in *.pdf
do
  pdftk "$f" output "tmp-$f" uncompress
  sed -i "s/1 1 1 RG/99 99 99 RG/g" "tmp-$f"
  sed -i "s/1 1 1 rg/99 99 99 rg/g" "tmp-$f"
  sed -i "s/[0-1] [0-1] [0-1] RG/0 0 0 RG/g" "tmp-$f"
  sed -i "s/[0-1] [0-1] [0-1] rg/0 0 0 rg/g" "tmp-$f"
  sed -i "s/0.[0-9]\+ 0.[0-9]\+ 0.[0-9]\+ RG/0 0 0 RG/g" "tmp-$f"
  sed -i "s/0.[0-9]\+ 0.[0-9]\+ 0.[0-9]\+ rg/0 0 0 rg/g" "tmp-$f"
  sed -i "s/99 99 99 RG/1 1 1 RG/g" "tmp-$f"
  sed -i "s/99 99 99 rg/1 1 1 rg/g" "tmp-$f"
  pdftk "tmp-$f" output "filled-$f" compress
  rm "tmp-$f"
done
