require.config({ paths: { 'vs': './node_modules/monaco-editor/min/vs' } });
require(['vs/editor/editor.main'], function () {

    // 初始化变量
    var fileCounter = 0;
    var editorArray = [];
    var defaultCode = [
        'function helloWorld() {',
        '   console.log("Hello world!");',
        '}'
    ].join('\n');
	
    // 定义编辑器主题
    // monaco.editor.defineTheme('myTheme', {
    //     base: 'vs',
    //     inherit: true,
        // rules: [{ background: 'EDF9FA' }],
        // colors: { 'editor.lineHighlightBackground': '#0000FF20' }
    // });
    // monaco.editor.setTheme('myTheme');
    // 新建一个编辑器
    function newEditor(container_id, code, language) {
        var model = monaco.editor.createModel(code, language);
        var editor = monaco.editor.create(document.getElementById(container_id), {
            model: model,
	        automaticLayout: true
        });
        editorArray.push(editor);
        return editor;
    }

    // 新建一个 div
    function addNewEditor(code, language) {
        var new_container = document.createElement("DIV");
        new_container.id = "container-" + fileCounter.toString(10);
        new_container.className = "container";
        document.getElementById("root").appendChild(new_container);
        newEditor(new_container.id, code, language);
        fileCounter += 1;
    }

    addNewEditor(defaultCode, 'typescript');

	// var LocalLoadLang = function (url, method) {
    //     var request = new XMLHttpRequest();
    //     return new Promise(function (resolve, reject) {
    //         request.onreadystatechange = function () {
    //             if (request.readyState !== 4) return;
    //             if (request.status >= 200 && request.status < 300) {
    //                 resolve(request);
    //             } else {
    //                 reject({
    //                     status: request.status,
    //                     statusText: request.statusText
    //                 });
    //             }
    //         };
    //         request.open(method || 'GET', url, true);
    //         request.send();
    //     });
	// };
    // LocalLoadLang('./node_modules/@types/frida-gum/index.d.ts').then(function (data) {
    //     alert(data.responseText)
    //     monaco.languages.typescript.typescriptDefaults.addExtraLib(data.responseText, '');
    // });

    

    

});