# Beat Saber Beatmap Downgrader

A cli tool to downgrade any Beat Saber beatmap written in difficulty file V3 to V2    

Thanks to the Beat Saber Modding Group for having the file formats wonderfully documented: https://bsmg.wiki/mapping/map-format.html

## Usage

You can use the `downgrader.py` script on a single beatmap folder and it will create a downgraded version of that beatmap next to it.

```
python downgrader.py C:\absolute\path\to\beatmap
```



The `auto_downgrade.py` script is supposed make the use easier. Once set up, it will downgrade any new maps that were downloaded to your Beat Saber folder since it last ran and delete the original one.

To set it up just run `setup.py` and follow the instructions. If you changed your mind on your inputs just run `setup.py` again.