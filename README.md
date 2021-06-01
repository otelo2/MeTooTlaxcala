# MeTooTlaxcala

## Backend

### Instalación:

Empieza en tu directorio home 

```cd ~```

Clonar el repositorio.

Entrar a la carpeta clonada y correr: 
  ```pip3 -r requirements.txt```
  
### Archivo keys.py:

Crea un nuevo archivo llamado keys.py con la siguiente estructura:

```
apiKey = "<25 chars>"
apiSecret = "<50 chars>"
bearerToken = "<112 chars>"
accessToken = "<50 chars>"
accessTokenSecret = "<45 chars>"
```
Sustituyendo <X chars> por tu clave de API de Twitter.
  
### Archivo dbKeys.py:

Crea un nuevo archivo llamado keys.py con la siguiente estructura:

```
DB_HOST = "<host remoto o localhost>"
DB_NAME = "MeTooTlaxcala"
DB_USER = "<postgres u otro usuario>"
DB_PASS = "<contraseña de db>"
```
Se ponen los valores según esté hecha la base de datos. Contacta al administrador de la base de datos para obtener esta información

### Para poner la descarga y push automático:

Descarga de Tweets automática (Sólo Linux):
```crontab -e ```
    
En la última linea del archivo que se abre añadir:
    
```5 0 * * * cd /home/<tu_usuario>/MeTooTlaxcala && /home/<tu_usuario>/MeTooTlaxcala/main.py >> ~/cron.log 2>&1```
    
Esto va a correr el programa cada día a las 12:05am.


### Backup a GitHub:

```git config credential.helper store```

```git pull```

Ahora te va a pedir tus credenciales de github. Se hace para que las guarde y no las pida cada vez.
  
  Nota: Si tienes activado 2FA, necesitarás hacer esto del token en vez de tu contraseña: https://stackoverflow.com/questions/17659206/git-push-results-in-authentication-failed

Añadimos al crontab el archivo gitBackup.sh

```contab -e ```

En la última linea del archivo que se abre añadir:

```10 0 * * * /home/<tu_usuario>/MeTooTlaxcala/gitBackup.sh >> ~/gitBackup.log 2>&1```

Esto va a hacer el backup a git cada día a las 12:10am.
  
  
### Sincronizar con GitHub:  
Para que el repositorio automaticamente se actualice a la versión más reciente.
Se hace cada día a media noche.
  
  ```contab -e ```
  
  Añadimos al archivo que se abre:
  
  ```1 0 * * * /home/<tu_usuario>/MeTooTlaxcala/gitPull.sh >> ~/gitPull.log 2>&1```
  
  ### Crontab completo
A la fecha, el crontab completo se ve así:
  ```
  1 0 * * * /home/<tu_usuario>/MeTooTlaxcala/gitPull.sh >> ~/gitPull.log 2>&1
  5 0 * * * cd /home/<tu_usuario>/MeTooTlaxcala && /home/pi/MeTooTlaxcala/main.py >> ~/mainCron.log 2>&1
  10 0 * * * /home/<tu_usuario>/MeTooTlaxcala/gitBackup.sh >> ~/gitBackup.log 2>&1
