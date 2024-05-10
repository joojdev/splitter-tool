import os
import hashlib
import sys
import math

print()
map_name = input('  Qual o .map que você quer descompactar? ')

print()
if not os.path.isfile(map_name):
  print('  Este arquivo não existe ou é uma pasta!')
  sys.exit(0)

parts_folder = input('  Onde estão os arquivos de partes do arquivo? ')

print()
if not os.path.isdir(parts_folder):
  print('  Esta pasta não existe ou é um arquivo!')
  sys.exit(0)

map_file = open(map_name, 'r')
[filename, part_list] = map_file.read().split('|')
parts = part_list.split('/')
map_file.close()

parts_filename_list = [f'{(_.split(":")[0])}.part' for _ in parts]
checksum_list = [(_.split(':')[1]) for _ in parts]

if not set(parts_filename_list).issubset(set([_ for _ in os.listdir(parts_folder) if _.endswith('.part')])):
  print('  Algo aconteceu e nem todos os arquivos estão presentes!')
  sys.exit(0)

checked_checksum_list = [hashlib.md5(open(f'{parts_folder}/{_}', 'rb').read()).hexdigest() for _ in parts_filename_list]

if checksum_list != checked_checksum_list:
  print()
  print('  O arquivo foi danificado e não foi possível descompactá-lo!')
  sys.exit()

file = open(filename, 'wb')

for part_filename in parts_filename_list:
  part_path = f'{parts_folder}/{part_filename}'
  part_size = os.stat(part_path).st_size
  part_file = open(part_path, 'rb')

  buffer_size = min(part_size, 4096)
  iterations = math.ceil(part_size / buffer_size)

  for iteration in range(iterations):
    content = part_file.read(buffer_size)
    file.write(content)
  part_file.close()
file.close()