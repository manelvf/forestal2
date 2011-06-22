file="oficina"
backup_dir="../backups"

rm ${backup_dir}/$(date +%A)
cp ${file} ${backup_dir}/$(date +%A)


