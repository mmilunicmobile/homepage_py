/* @refresh reload */
import { createSignal } from 'solid-js';

const CustomQuote = (props, values) => {
  const quotes = [
    "\"The greatest glory in living lies not in never falling, but in rising every time we fall.\" - Nelson Mandela",
    "\"If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success.\" - James Cameron",
    "\"The only way to do great work is to love what you do.\" - Steve Jobs",
    "\"The best way to predict the future is to create it.\" - Alan Kay",
    "\"We can't help everyone. We can't help one specific person. But if you help one person, it will help them all.\" - John D. Rockefeller",
    "\"Success usually comes to those who are too busy to be looking for it.\" - Henry David Thoreau",
    "\"It is never too late to be what you might have been.\" - George Eliot",
    "\"Success is not finals, failure is not fatal: it is the courage to continue that counts.\" - Winston Churchill",
    "\"The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.\" - W. Clement Stone",
  ]
  const [index, setIndex] = createSignal(0);
  const quote = () => quotes[index()];
  const increment = () => setIndex((prev) => (prev + 1) % quotes.length);


  if (!import.meta.env.SSR) {
    const { element } = values
    element.renderRoot.innerHTML = ""
  }

  return (
    <div onclick={increment}>
      {quote()}
    </div>
  );
};

const element_name = 'spanish-quote'

export { element_name, CustomQuote as element }



