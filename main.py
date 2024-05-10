import sys

try:
  print()
  print('  -= Splitting Tool by joojdev =-')
  print()
  print('  1. Splitter')
  print('  2. Merger')
  print()
  try:
    option = int(input('  Qual ferramenta você deseja utilizar? '))
  except ValueError:
    print()
    print('  O número da opção precisa ser necessariamente um número!')
    sys.exit(0)

  if option not in [1, 2]:
    print('  O número tem que corresponder com as opções presentes no menu!')
    sys.exit(0)

  if option == 1:
    import split
  else:
    import merge
except KeyboardInterrupt:
  print()
  print('  Saindo...')