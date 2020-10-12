module.exports = {
  // future: {
  //   removeDeprecatedGapUtilities: true,
  //   purgeLayersByDefault: true,
  // },
  // purge: { mode: "all", content: ["./../../templates/*.html"] },
  theme: {
    colors: {
      trans: "transparent",

      white: "#ffffff",
      black: "#061A37",
      "gray-dark": "#5C5C5C",
      gray: "#e5e5e5",
      "gray-light": "#F5F5F5",
      pri: "#317BE8",
      // "pri-dark": "#061A37",
      "pri-light": "#D3EBEE",
      sec: "#EF6C00",
      "sec-light": "#FFDDC2",
      dg: "#E53E3E",
      "dg-light": "#FED7D7",
      suc: "#38A169",
      "suc-light": "#C6F6D5",
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    extend: {
      width: {
        mc: "max-content",
        76: "20rem",
        96: "24rem",
        120: "32rem",
        160: "42rem",
        192: "48rem",
      },
      height: {
        96: "24rem",
        120: "32rem",
      },
      borderRadius: {
        extra: "2rem",
      },
      minWidth: {
        32: "8rem",
      },
      maxHeight: {
        64: "16rem",
      },
    },
  },
  variants: {},
  plugins: [require("tailwindcss"), require("autoprefixer")],
};
