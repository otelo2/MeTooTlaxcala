# MeTooTlaxcala

## Backend

### Instalación:

Empieza en tu directorio home 

```cd ~```

Clonar el repositorio.

Entrar a la carpeta clonada y correr: 
  ```pip3 -r requirements.txt```
  
Para poner la descarga y push automático:

Descarga de Tweets automática (Sólo Linux):
```crontab -e ```
    
En la última linea del archivo que se abre añadir:
    
```5 0 * * * cd /home/<tu_usuario>/MeTooTlaxcala && /home/<tu_usuario>/MeTooTlaxcala/tweetDownloader.py >> ~/cron.log 2>&1```
    
Esto va a correr el programa cada día a las 12:05am.


Backup a GitHub:

```git config credential.helper store```

```git pull```

Ahora te va a pedir tus credenciales de github. Se hace para que las guarde y no las pida cada vez.

Añadimos al crontab el archivo gitBackup.sh

```contab -e ```

En la última linea del archivo que se abre añadir:

```10 0 * * * /home/<tu_usuario>/MeTooTlaxcala/gitBackup.sh```

Esto va a hacer el backup a git cada día a las 12:10am.
