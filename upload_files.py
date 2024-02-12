import pexpect
import sys

if len(sys.argv) != 2:
    print("Uso: python3 upload_files.py <nome_da_rasp>")
    sys.exit(1)

rasp_name = sys.argv[1]

# copiar server central:
cmd_central = f'scp -r central {rasp_name}:~/projeto_1'
child = pexpect.spawn(cmd_central)
child.expect("password:")
child.sendline("190037997")

child.expect(pexpect.EOF)

# copiar server 1
cmd_server1 = f'scp -r server1 {rasp_name}:~/projeto_1'
child = pexpect.spawn(cmd_server1)
child.expect('password:')
child.sendline('190037997')

child.expect(pexpect.EOF)

#copiar server 2
cmd_server2 = f'scp -r server2 {rasp_name}:~/projeto_1'
child = pexpect.spawn(cmd_server2)
child.expect('password:')
child.sendline('190037997')

child.expect(pexpect.EOF)

#copiar config
cmd_config = f'scp -r modelconfig {rasp_name}:~/projeto_1'
child = pexpect.spawn(cmd_config)
child.expect('password:')
child.sendline('190037997')

child.expect(pexpect.EOF)

print("Arquivos copiados!")

# # Copiar main.py
# cmd_main = f"scp -r main.py {rasp_name}:~/projeto_1"
# child = pexpect.spawn(cmd_main)
# child.expect("password:")
# child.sendline("190037997")

# # Aguarda conclusão antes de continuar
# child.expect(pexpect.EOF)

# # Copiar os arquivos dentro do diretório src/
# cmd_src = f"scp -r src {rasp_name}:~/projeto_1"
# child = pexpect.spawn(cmd_src)
# child.expect("password:")
# child.sendline("190037997")

# # Aguardar a cópia ser concluída antes de continuar
# child.expect(pexpect.EOF)

# print("Arquivos copiados com sucesso!")
