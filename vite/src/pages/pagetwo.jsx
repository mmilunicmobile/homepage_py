/* @refresh reload */
import { element_name, element } from '../web-components/customQuote.jsx';
import { customElement } from 'solid-element';

if (!import.meta.env.SSR) {
    customElement(element_name, element);
}

export default { [element_name]: element }

