/* @refresh reload */
import { customElement } from 'solid-element';
import { element_name, element, CountQuote } from '../web-components/customQuote.jsx';
import CodeQuote from '../web-components/customQuote.jsx';

if (!import.meta.env.SSR) {
    customElement(element_name, { "name": "" }, element);
    customElement("code-quote", CodeQuote);
    customElement("count-quote", CountQuote);
}

export default { [element_name]: element, "code-quote": CodeQuote, "count-quote": CodeQuote }