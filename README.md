# <img src="https://github.com/B611/MSC_Darknet_Markets/blob/master/app/gui/src/icons/spider.svg" width="48"> Nyja, the Dark Web sensing toolkit

Nyja is a modular toolkit designed to help researchers study the Tor network.

It is a cross-platform and user-friendly toolkit that allows researchers to conduct massive metadata gathering, timestamp-based archiving of websites, scheduled monitoring of indexing websites for automatic discovery of .onion links, and much more.

In order to run nyja, the only required dependency is having Docker installed and running.
You can install Docker Desktop by clicking [this link.](https://www.docker.com/products/docker-desktop)

---

# CLI + GUI Demo

![Nyja CLI](files/nyja_CLI.svg)



---

## Running the CLI
The CLI is a fish command-line interface with autocomplete allowing to quickly interact with nyja for advanced users.

Running the script in the _launchers_ folder will start the project, create a node on the Tor network, and start services such as MongoDB.

If you want to run the CLI on GNU/Linux :
```
$ ./launchers/unix/run_cli.sh
```
Or on Windows :
```
$ ./launchers/windows/run_cli.bat
```

You will then land in a fish shell, in our custom environment. The tool can be interacted with following the help, using different commands.

For example, get the list of onion websites present on https://dark.fail and output them locally without saving in database :
```
$ nyja crawl "https://dark.fail" --output
```

## Running the GUI
The Web Application is designed to use nyja through an easy to use interface via your web browser.

Running the script in the launchers folder will start the project, create a node on the Tor network, and start services such as MongoDB.

If you want to run the Web Application on GNU/Linux :
```
$ ./launchers/unix/run_web.sh
```
Or on Windows :
```
$ ./launchers/windows/run_web.bat
```

It will then open a nyja GUI in your default web browser.

# Browser Compatibility
<img src="https://i.nuuls.com/_YEEl.png">

Made with ❤ by [Gabriel](https://www.linkedin.com/in/gabriel-ruaud/), [Louis](https://www.linkedin.com/in/louisanelli/) and [Robin](https://www.linkedin.com/in/Rob2n/)
