{
if($1 ~ /\*SECTION/){
getline
while ($1 !~ /\*/){
getline
}
}
print $0
}