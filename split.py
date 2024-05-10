import os
import sys
from uuid import uuid4
import hashlib
import math
from datetime import datetime

def get_random_name():
  return ''.join(str(uuid4()).split('-'))

print()
filename = input('  Digite o caminho do arquivo: ')

print()
if not os.path.isfile(filename):
  print('  Esse arquivo não existe ou é uma pasta!')
  sys.exit(0)

file_size = os.stat(filename).st_size

try:
  print('  Como deseja dividir?')
  print()
  print('  1. Quantidade de setores')
  print('  2. Tamanho')
  print()
  option = int(input('  > '))
except ValueError:
  print()
  print('  A opção precisa ser necessariamente um número!')
  sys.exit(0)

print()
if option not in [1, 2]:
  print('  A opção tem que ser um ou 2.')
  sys.exit(0)

if option == 1:
  try:
    sectors = int(input('  Quantos setores vão ser? '))
  except ValueError:
    print()
    print('  A quantidade de setores precisa ser necessariamente um número!')
    sys.exit(0)

  if sectors < 2:
    print()
    print('  A quantidade de setores tem que ser maior do que um!')
    sys.exit(0)

  sector_size = file_size // sectors
else:
  try:
    sector_size = int(input('  Quantos bytes vão ser por setor? '))
  except ValueError:
    print()
    print('  A quantidade de bytes por setor precisa ser necessariamente um número!')
    sys.exit(0)
  
  if sector_size < 1:
    print()
    print('  A quantidade de bytes por setor tem que ser maior do que 0!')
    sys.exit(0)

  sectors = math.ceil(file_size / sector_size)

file = open(filename, 'rb')
order = []

output_folder = f'{filename}-{int(datetime.timestamp(datetime.now()))}'
os.mkdir(output_folder)

for index in range(sectors):
  random = get_random_name()
  random_filename = f'{output_folder}/{random}.part'
  part = open(random_filename, 'wb')

  if index == sectors - 1:
    sector_size += file_size % sectors

  buffer_size = min(sector_size, 4096)
  iterations = math.ceil(sector_size / buffer_size)
  last_has_decimal = iterations != sector_size // buffer_size

  for iteration in range(iterations):
    if last_has_decimal and iteration == iterations - 1:
      buffer_size = sector_size % buffer_size

    part.write(file.read(buffer_size))
  part.close()
  checksum = hashlib.md5(open(random_filename, 'rb').read()).hexdigest()
  order.append((random, checksum))
file.close()

part_list = open(f'{output_folder}/{filename}.map', 'w')
part_list.write(filename + '|' + '/'.join([f'{_[0]}:{_[1]}' for _ in order]))
part_list.close()