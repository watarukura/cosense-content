# watarukura
[https://gyazo.com/7ce691e558358b9ef4ffb948c6229036](https://gyazo.com/7ce691e558358b9ef4ffb948c6229036)

[https://lh4.googleusercontent.com/-mq81LQ2Mcak/AAAAAAAAAAI/AAAAAAAAAE8/WwV-CRc7vCc/photo.jpg](https://lh4.googleusercontent.com/-mq81LQ2Mcak/AAAAAAAAAAI/AAAAAAAAAE8/WwV-CRc7vCc/photo.jpg)

this is watarukura’s  scrapbox

Link

- github https://github.com/watarukura
- wantedly https://www.wantedly.com/users/8180928
- qiita https://qiita.com/watarukura

```script.js
setTimeout(() => {
 	// チェックボックスとして使用する文字セットのリスト
 	const checkboxSetList = [
 		['⬜', '✅'],
 		['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'],
 		['😀', '😐', '😧', '😨']
 	];

 	/*
 		['⬜', '✅']
 		['🔲', '☑️']
 	*/

 	const allBoxes = checkboxSetList.reduce((accu, current) => accu.concat(current), []);
 	const startsWithBoxReg = new RegExp('^\\s*(' + allBoxes.join('|') + ')');
 	const targetProject = scrapbox.Project.name;

 	class KeydownEvent {
 		constructor() {
 			this.textArea = document.getElementById('text-input');
 			this.event = document.createEvent('UIEvent');
 			this.event.initEvent('keydown', true, true);
 		}
 		dispatch(keyCode, withShift = false, withCtrl = false, withAlt = false, withCommand = false) {
 			this.event.keyCode = keyCode;
 			this.event.shiftKey = withShift;
 			this.event.ctrlKey = withCtrl;
 			this.event.altKey = withAlt;
 			this.event.metaKey = withCommand;
 			this.textArea.dispatchEvent(this.event);
 		}
 	}

 	// ボックスクリックでオンオフする
 	$('#app-container').off(`click.toggleCheckBox_${targetProject}`, '.lines');
 	$('#app-container').on(`click.toggleCheckBox_${targetProject}`, '.lines', async event => {
 		if (scrapbox.Project.name !== targetProject) {
 			$('#app-container').off(`click.toggleCheckBox_${targetProject}`, '.lines');
 			return;
 		}
 		const target = event.target;
 		if (!isFirstElementChild(target)||!isCharSpan(target, allBoxes)) return;
 		await new Promise(resolve => setTimeout(resolve, 30));
 		let lineString;
 		try {
 			lineString = getCursorLineString();
 		} catch (err) {
 			console.log(err);
 			return;
 		}
 		if (!startsWithBoxReg.test(lineString)) return;
 		const targetX = target.getBoundingClientRect().left;
 		const cursorX = document.getElementsByClassName('cursor')[0].getBoundingClientRect().left;
 		const keydownEvent = new KeydownEvent();
 		if (cursorX <= targetX) {
 			keydownEvent.dispatch(39);  // →
 		}
 		keydownEvent.dispatch(8);  // Backspace
 		const newBox = (() => {
 			const trimmedLineString = lineString.trim();
 			for (const checkboxSet of checkboxSetList) {
 				for (let i = 0; i < checkboxSet.length; i++) {
 					if (trimmedLineString.startsWith(checkboxSet[i])) {
 						return checkboxSet[i + 1 < checkboxSet.length ? i + 1 : 0];
 					}
 				}
 			}
 			return target.textContent;
 		})();
 		writeText(newBox);

 		// この下のコメントアウトを解除すると、checked時に取消線を入れて時刻を追記します
 		// Mac、Porterでのみ動作します
 		/*
 		if (/Mobile/.test(navigator.userAgent)) return;
 		const targetBoxSet = checkboxSetList[0];
 		if (!targetBoxSet.includes(newBox) || newBox === targetBoxSet[0]) return;
 		await new Promise(resolve => setTimeout(resolve, 30));
 		keydownEvent.dispatch(39, true, false, false, true);  // shift + command + →
 		writeText('-');
 		keydownEvent.dispatch(39, false, false, false, true);  // command + →
 		const now = moment().format('HH:mm');
 		writeText(` ${now}`);
 		*/
 	});

 	// ボックス行で改行すると次行にボックス自動挿入
 	$('#text-input').off(`keydown.autoInsertCheckBox_${targetProject}`);
 	$('#text-input').on(`keydown.autoInsertCheckBox_${targetProject}`, async event => {
 		if (scrapbox.Project.name !== targetProject) {
 			$('#text-input').off(`keydown.autoInsertCheckBox_${targetProject}`);
 			return;
 		}
 		switch (event.key) {
 			case 'Enter': {
 				let currentLineString;
 				try {
 					currentLineString = getCursorLineString();
 				} catch (err) {
 					console.log(err);
 					return;
 				}
 				if (!startsWithBoxReg.test(currentLineString)) return;
 				await new Promise(resolve => setTimeout(resolve, 30));
 				let nextLineString;
 				try {
 					nextLineString = getCursorLineString();
 				} catch (err) {
 					console.log(err);
 					return;
 				}
 				if (!startsWithBoxReg.test(nextLineString)) {
 					const trimmedLineString = currentLineString.trim();
 					const targetBoxSet = checkboxSetList.find(boxSet => {
 						return boxSet.some(box => trimmedLineString.startsWith(box));
 					});
 					writeText(targetBoxSet[0]);	
 				}
 				return;
 			}
 			default: {
 				return;
 			}
 		}
 	});

 	function isFirstElementChild(element) {
 		return element.parentNode.firstElementChild === element;
 	}
 	function getCursorLineString() {
 		return document.querySelector('.lines div.line.cursor-line').textContent;
 	}
 	function isCharSpan(element, targetCharList) {
 		return element.tagName === 'SPAN'
 			&& targetCharList.includes(element.textContent)
 			&& element.classList.value.split(' ').some(value => /^c\-\d+$/.test(value));
 	}
 	function writeText(text) {
 		const textArea = document.getElementById('text-input');
 		textArea.value = text;
 		textArea.dispatchEvent(new InputEvent('input', {bubbles: true, cancelable: true}));
 	}
 }, 1500);

```
```script.css
body {background-color:black;}
```
[#member](member)
