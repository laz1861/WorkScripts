for i in  {1..96}
do
  convert -verbose basemap2.png "$(printf "feeder%07d.png" "$i")" -composite  "$(printf "result%07d.png" "$i")"
done;
