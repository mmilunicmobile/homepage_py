import { renderToStringAsync, Dynamic } from 'solid-js/web'
import fs from 'node:fs';

function serverRender(element, component, element_params) {
    return <Dynamic component={element} {...element_params}><template shadowrootmode="open"><Dynamic component={component} {...element_params} /></template></Dynamic>

    // return renderToString(() => <custom-quote><template shadowrootmode="open"><CustomQuote /></template></custom-quote>)
}

async function customElementPrefill(element_name, element, element_params) {
    const customQuote = await renderToStringAsync(() => serverRender(element_name, element, element_params));

    return customQuote
}

const output_rendered = {}

const output_components = {}

const modules = import.meta.glob('./src/pages/*.jsx')


for (const path in modules) {
    const mod = await modules[path]()
    output_rendered[path] = {}
    output_components[path] = {}
    for (const element_name in mod.default) {
        output_rendered[path][element_name] = await customElementPrefill(element_name, mod.default[element_name])
        output_components[path][element_name] = mod.default[element_name]
        // console.log(JSON.stringify(output[path][element_name]))
    }
}

if (process.argv.length === 5) {
    const script_name = process.argv[2]
    const element_name = process.argv[3]
    const element_params = JSON.parse(process.argv[4])
    console.log(await customElementPrefill(element_name, output_components[script_name][element_name], element_params))
}

if (process.argv.length === 2) {
    fs.writeFileSync('./dist/server/.vite/customElements.json', JSON.stringify(output_rendered));
}