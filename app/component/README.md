## Streamlit Confetti Component

The component uses the [JSConfetti](https://github.com/loonywizard/js-confetti) library.

The component tried to show the confetti on parent window through embedded iframe. It means it can not be debuged with local `npm run start` procedure. Otherwise you will see this kind of message:

```
Blocked a frame with origin from accessing a cross-origin frame.
Protocols, domains, and ports must match.
```

Good [tutorial](https://towardsdatascience.com/how-to-create-custom-streamlit-components-de6a00a7d5ab) how to create the Streamlit Custom Components.

The following commands should help with `npm install` issues:

```bash
npm cache clean --force
npm set maxsockets 3
npm config set registry http://registry.npmjs.org/
npm install --legacy-peer-deps --verbose
```
