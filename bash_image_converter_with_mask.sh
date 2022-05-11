for file in  feeder*.png; do
  convert -verbose "$file" -mask mask.png -alpha set -channel A -evaluate multiply 0.5 +channel -set filename:f '%t' compose_test/'%[filename:f].png' 
done;
