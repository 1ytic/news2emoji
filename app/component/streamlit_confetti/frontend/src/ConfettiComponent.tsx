import {
  // Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import { ReactNode } from "react"
import JSConfetti from "js-confetti"


function clearCanvas() {
  const body = window.parent.document.body;
  const elements = body.getElementsByTagName("canvas");
  for (var i = 0; i < elements.length; i++) {
    try {
      body.removeChild(elements[i]);
    } catch (err) {
    }
  }
}


function createCanvas(): HTMLCanvasElement {

  const canvas = document.createElement("canvas")

  canvas.style.position = "fixed"
  canvas.style.width = "100%"
  canvas.style.height = "100%"
  canvas.style.top = "0"
  canvas.style.left = "0"
  canvas.style.zIndex = "1000"
  canvas.style.pointerEvents = "none"

  window.parent.document.body.appendChild(canvas)

  return canvas
}

/**
 * This is a React-based custom component. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class ConfettiComponent extends StreamlitComponentBase {

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "emojis" arg.
    const emojis = this.props.args["emojis"]

    clearCanvas();

    if (emojis !== null) {
      const canvas = createCanvas();
      const jsConfetti = new JSConfetti({ canvas });
      for (const row of emojis) {
        const scale = Math.round(row["score"] * 100 * 1.5);
        jsConfetti.addConfetti({
          emojis: [row["emoji"]],
          emojiSize: Math.min(100, Math.max(50, scale)),
          confettiNumber: Math.min(100, Math.max(10, scale)),
        })
      }
    }

    // Streamlit.setComponentValue(null);

    return ""
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don"t need to edit withStreamlitConnection (but you"re welcome to!).
export default withStreamlitConnection(ConfettiComponent)
