
# Mill - scala build tools for the better good

- Creator: [Li Haoyi](https://github.com/lihaoyi)<br>
- [Documentation](https://com-lihaoyi.github.io/mill/mill/Intro_to_Mill.html)<br>
- [Repository](https://github.com/com-lihaoyi/mill)<br>

### My build template
- Modules Utilized: buildinfo, docker, Scalafix, versionfile
- Scoverage module has stopped working once I added crossversion support. will need to revisit / resolve
```sh
wget https://raw.githubusercontent.com/cjdonaldson/cjdonaldson/main/mill/build.sc
```

### Mill tasks
```sh
mill inpspect __  # double underscore
mill inpspect moduleName
mill resolve _
mill resolve __
mill clean
mill __.compile
mill __.test
mill __.scoverage.htmlReport
mill __.reformat
mill __.publishLocal
mill all __.{compile,run}
mill -w __.compile
mill -w __.test
mill module1.reformat
mill module1.scoverage.compile
mill module1.scoverage.htmlReport

# zsh makes these more difficult as the param must be wraped in `"`
mill [-w] module1[2.12].compile
mill [-w] module1[2.12].run
mill [-w] module1[2.12].runBackground
mill [-w] module1[2.12].launcher
mill [-w] module1[2.12].jar
mill [-w] module1[2.12].assembly
mill -i module1[2.13].console
mill -i module1[2.13].repl
```
