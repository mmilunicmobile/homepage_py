import { renderToStringAsync, Dynamic } from 'solid-js/web'
import fs from 'node:fs';

function serverRender(element, component) {
    return <Dynamic component={element}><template shadowrootmode="open"><Dynamic component={component} /></template></Dynamic>

    // return renderToString(() => <custom-quote><template shadowrootmode="open"><CustomQuote /></template></custom-quote>)
}

async function customElementPrefill(element_name, element) {
    const customQuote = await renderToStringAsync(() => serverRender(element_name, element));

    return customQuote
}

const output = {}

const modules = import.meta.glob('./src/pages/*.jsx')


for (const path in modules) {
    const mod = await modules[path]()
    output[path] = {}
    for (const element_name in mod.default) {
        output[path][element_name] = await customElementPrefill(element_name, mod.default[element_name])
        console.log(JSON.stringify(output[path][element_name]))
    }
}

fs.writeFileSync('./dist/server/.vite/customElements.json', JSON.stringify(output));