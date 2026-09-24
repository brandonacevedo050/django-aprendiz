Copia aquí tu archivo .sql existente (el dump que ya tenías en
Mysql-init/ del proyecto anterior, con la tabla 'aprendiz' y sus
datos). MySQL lo ejecuta automáticamente la primera vez que el
volumen "mysql_data" está vacío.

Este backend en Django está construido para respetar exactamente ese
esquema (ver aprendiz/models.py y aprendiz/migrations/0001_initial.py),
así que no hace falta modificar tu dump existente.
