import re
import time
import matplotlib.pyplot as plt
start=time.time()
msj_t=[]
msj_l=[]
media_t=[]
media_l=[]
nodate_msj_l=[]
nodate_msj_t=[]
words_t={}
words_l={}
print('''Hola!

Para usar este programa, abrí una conversación,
tocá los tres puntitos, tocá 'Más',
tocá "Exportar Chat" y elegí "Sin Multimedia".
Mandalo a la PC (en la misma carpeta que este programa).
''')
file_name=str(input('Copiá y pegá el nombre del .txt que exportaste (tiene que estar en la misma carpeta que este archivo):\n'))
if '.txt' in file_name:
    file_name=file_name.replace('.txt', '')
name_a=input('\nEscribí el nombre exacto del contacto que tenés agendado (sensible a las mayúsculas): \n').encode()
name_b=input('\nEscribí tu nombre de perfil (sensible a las mayúsculas): \n').encode()
print('\n\nProcesando... Esto puede llevar algunos minutos\n\n')
msj_name_a=b' - '+ name_a + b':'
msj_name_b=b' - '+ name_b + b':'
str_name_a=str(name_a.decode('utf-8','ignore'))
str_name_b=str(name_b.decode('utf-8','ignore'))
msj_per_month_l={}
msj_per_month_t={}



def contar(nodate_msj, words):
    net=[]
    ten=[]
    for y in nodate_msj:
        x=y.lower()
        vec = x.split()
        net.extend(vec)
    for x in net:
        if 'j' in  x:
            if 'a' in x:
                count=0
                for char in x:
                    if char=='j' or char=='a':
                        count+=1
                        if count<len(x):
                            continue
                        elif count==len(x):
                            x='*jaja'
        if x==b'':
            del(x)
        try:
          if len(x)>2:
            while x[len(x)-1]==x[len(x)-2]:
                x=x.replace(x[-1:],'',1)
        except:
            pass
        if x=='':
            del(x)
            continue
        ten.append(x)
    for x in ten:
        if x not in words:
          if not(x == '<media' or x=='omitted>' or x=='message' or x=='deleted' or x=='<multimedia' or x=='omitido>' or x=='media' or x=='omitted' or x=='multimedia' or x=='omitido'):
            words[x] = ten.count(x)

def mensajes_por_mes(msj_x, msj_per_month_x):
    for x in msj_x:
        date_pat='\d+\/\d+\/\d+'
        p=re.search(date_pat, x).group()
        month=re.search('^\d+', p).group()
        year=re.search('\d+$', p).group()
        key_name=month+'/'+year
        if msj_per_month_x.get(key_name)!=None:
            msj_per_month_x[key_name]+=1
        else:
            msj_per_month_x[key_name]=1
            




file=open(file_name+'.txt','rb')
read=file.readlines()
file.close()
file_2=open(file_name+'.txt','rb')
read_2=file_2.read()
file_2.close()
a=0
try:
    fecha=re.search(b'\d+\/\d+\/\d+', read[a]).group()
    fecha=fecha.decode('utf-8','ignore')
except TypeError:
    a+=1
#dos files separados, uno sin saltos de linea para los audios xq si se corta el media ommited no lo encuentra


for x in read:
    x=x.decode('utf-8','ignore')
    if str_name_a in x:
        msj_t.append(x)
    elif str_name_b in x:
        msj_l.append(x)
cant_l=len(msj_l)
cant_t=len(msj_t)
#detecta y cuenta los msj de cada uno


media_t=read_2.count(msj_name_a+b' <Media omitted>')
media_l=read_2.count(msj_name_b+b' <Media omitted>')
if media_t==0 and media_l==0:
    media_t=read_2.count(msj_name_a+b' <Multimedia omitido>')
    media_l=read_2.count(msj_name_b+b' <Multimedia omitido>')
#del otro archivo busca los audios y los cuenta


for x in msj_t:
    y=re.sub('\d.*:\s','',x)
    nodate_msj_t.append(y)
for x in msj_l:
    y=re.sub('\d.*:\s','',x)
    nodate_msj_l.append(y)
#le saco la fecha y el nombre a los msj


contar(nodate_msj_t, words_t)
contar(nodate_msj_l, words_l)

mensajes_por_mes(msj_l, msj_per_month_l)
mensajes_por_mes(msj_t, msj_per_month_t)


plt.figure(1, figsize=(7.2, 4.8))
plt.subplot(2,1,1)
plt.plot(list(msj_per_month_l.keys()), list(msj_per_month_l.values()),color='green')
plt.title('Mensajes por mes de '+str_name_b)
plt.xlabel('Mes/Año')
plt.ylabel('Cantidad de Msj')
plt.subplot(2,1,2)
plt.plot(list(msj_per_month_t.keys()), list(msj_per_month_t.values()), color='orange')
plt.title('Mensajes por mes de '+str_name_a)
plt.xlabel('Mes/Año')
plt.ylabel('Cantidad de Msj')

perc_l=100/sum(words_l.values())
perc_t=100/sum(words_t.values())



srt_l=sorted(words_l.items(), key=lambda x: x[1], reverse=True)
srt_t=sorted(words_t.items(), key=lambda x: x[1], reverse=True)
tot_words_l=sum(words_l.values())
tot_words_t=sum(words_t.values())

plt.figure(2, figsize=(7.2, 4.8))
plt.subplot(2,1,1)
x_val = [x[0] for x in srt_l if len(x[0])>4]
y_val = [(x[1]) for x in srt_l if len(x[0])>4]
plt.bar(x_val[:17], y_val[:17], align='center',color='green')
plt.ylabel('Repeticiones')
plt.xlabel('Palabras de '+str_name_b)
plt.title('Palabras mas repetidas de 4 o mas letras')
plt.subplot(2,1,2)
x_val = [x[0] for x in srt_t if len(x[0])>4]
y_val = [(x[1]) for x in srt_t if len(x[0])>4]
plt.bar(x_val[:17], y_val[:17], align='center',color='orange')
plt.ylabel('Repeticiones')
plt.xlabel('Palabras de '+str_name_a)

plt.figure(3, figsize=(7.2, 4.8))
plt.subplot(2,1,1)
x_val = [x[0] for x in srt_l]
y_val = [(x[1]) for x in srt_l]
plt.bar(x_val[:17], y_val[:17], align='center',color='green')
plt.ylabel('Repeticiones')
plt.xlabel('Palabras de '+str_name_b)
plt.title('Palabras mas repetidas (Neto)')
plt.subplot(2,1,2)
x_val = [x[0] for x in srt_t]
y_val = [(x[1]) for x in srt_t]
plt.bar(x_val[:17], y_val[:17], align='center',color='orange')
plt.ylabel('Repeticiones')
plt.xlabel('Palabras de '+str_name_a)

plt.figure(4, figsize=(7.2, 4.8))
plt.subplot(2,1,1)
x_val = [x[0] for x in srt_l]
y_val = [perc_l*float(x[1]) for x in srt_l]
plt.bar(x_val[:17], y_val[:17], align='center',color='green')
plt.ylabel('%')
plt.xlabel('Palabras de '+str_name_b)
plt.title('Palabras mas repetidas (Porcentual)')
plt.subplot(2,1,2)
x_val = [x[0] for x in srt_t]
y_val = [perc_t*float(x[1]) for x in srt_t]
plt.bar(x_val[:17], y_val[:17], align='center',color='orange')
plt.ylabel('%')
plt.xlabel('Palabras de '+str_name_a)


print('\nDesde el '+ fecha +', '+str_name_a+' mandó: '+str(cant_t)+' mensajes (sin contar audios).')
print(str_name_b+', en cambio, mandó: '+str(cant_l)+' mensajes (sin contar audios).')
if cant_t>cant_l:
    dif=cant_t-cant_l
    print(str_name_a+' mandó '+str(dif)+' mensajes mas que '+str_name_b)
elif cant_l>cant_t:
    dif=cant_l-cant_t
    print(str_name_b+' mandó '+str(dif)+' mensajes mas que '+str_name_a)
print('\nDesde el '+ fecha +',' +str_name_a+' mandó: '+str(media_t)+' audios/fotos.')
print(str_name_b+', en cambio, mandó: '+str(media_l)+' audios/fotos.')
if media_t>media_l:
    dif=media_t-media_l
    print(str_name_a+' mandó '+str(dif)+' audios/fotos mas que '+str_name_b)
elif media_l>media_t:
    dif=media_l-media_t
    print(str_name_b+' mandó '+str(dif)+' audios/fotos mas que '+str_name_a)
print('\nEn total, '+str_name_a+' envió '+str(tot_words_t)+ ' palabras.')
print(str_name_b+', en cambio, envió '+str(tot_words_l)+ ' palabras.')
if tot_words_t>tot_words_l:
    dif=tot_words_t-tot_words_l
    print(str_name_a+' mandó '+str(dif)+' palabras más que ' +str_name_b)
elif tot_words_l>tot_words_t:
    dif=tot_words_l-tot_words_t
    print(str_name_b+' mandó '+str(dif)+' palabras más que ' +str_name_a)
#printeo de todos los datos de antes

# plt.figure(5, figsize=(7.2,4.8))
# plt.pie([tot_words_l,tot_words_t],explode=(0,0), labels=(str_name_b, str_name_a))

end=time.time()
print('\nTardó '+str(round(end-start, 3))+' segundos')

input('Tocá Enter para pasar a los gráficos, si los queres guardar, tocá el disquette')
plt.show()