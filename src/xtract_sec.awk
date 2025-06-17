{
# extract section only
if($1 ~ /\*SECTION/){
print $0
getline
while ($1 !~ /\*/){
print $0
getline
}
}
}