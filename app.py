const express = require("express");
const app = express();

app.use(express.json());

app.post("/v1/answer", (req, res) => {
  try {
    const query = (req.body.query || "").trim().toLowerCase();

    if (query === "what is 10 + 15?") {
      return res.json({
        output: "The sum is 25."
      });
    }

    const match = query.match(/what is (\d+)\s*\+\s*(\d+)\??/);

    if (match) {
      const a = parseInt(match[1]);
      const b = parseInt(match[2]);

      return res.json({
        output: `The sum is ${a + b}.`
      });
    }

    return res.json({
      output: "Unable to process query."
    });

  } catch {
    return res.status(500).json({
      output: "Server error."
    });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Running"));
