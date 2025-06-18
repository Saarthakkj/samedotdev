require("dotenv").config();
import express from "express";
// import Anthropic from "@anthropic-ai/sdk";
import { BASE_PROMPT, getSystemPrompt } from "./prompts";
// import { ContentBlock, TextBlock } from "@anthropic-ai/sdk/resources";
import {basePrompt as nodeBasePrompt} from "./defaults/node";
import {basePrompt as reactBasePrompt} from "./defaults/react";
import {generateText} from "ai";
import {google} from "@ai-sdk/google";
import cors from "cors";
import path from "path" ;
import dotenv from "dotenv" ; 

dotenv.config({
    path : path.resolve(__dirname , "../../.env")
})



//  import { generateText } from "ai"
// import { anthropic } from "@ai-sdk/anthropic"
// const { text } = await generateText({
// model: anthropic("claude-3-5-sonnet-latest"),
// prompt: "What is love?"
// })

// const anthropic = new Anthropic();



const app = express();
app.use(cors())
app.use(express.json())

app.post("/template", async (req, res) => {
    const prompt = req.body.prompt;
    
    // const response = await anthropic.messages.create({
    //     messages: [{
    //         role: 'user', content: prompt
    //     }],
    //     model: 'claude-3-5-sonnet-20241022',
    //     max_tokens: 200,
    //     system: "Return either node or react based on what do you think this project should be. Only return a single word either 'node' or 'react'. Do not return anything extra"
    // })

    const {text : answerRaw } = await generateText({
        model : google("gemini-2.0-flash-exp") ,
        prompt , 
        system : "Return either node or react based on what do you think this project should be. Only return a single word either 'node' or 'react'. Do not return anything extra"
        , maxTokens : 200
    })



    // const answer = (response.content[0] as TextBlock).text; // react or node

    const answer = answerRaw.trim().toLowerCase();

    if (answer == "react") {
        res.json({
            prompts: [BASE_PROMPT, `Here is an artifact that contains all files of the project visible to you.\nConsider the contents of ALL files in the project.\n\n${reactBasePrompt}\n\nHere is a list of files that exist on the file system but are not being shown to you:\n\n  - .gitignore\n  - package-lock.json\n`],
            uiPrompts: [reactBasePrompt]
        })
        return;
    }


    if (answer === "node") {
        res.json({
            prompts: [`Here is an artifact that contains all files of the project visible to you.\nConsider the contents of ALL files in the project.\n\n${reactBasePrompt}\n\nHere is a list of files that exist on the file system but are not being shown to you:\n\n  - .gitignore\n  - package-lock.json\n`],
            uiPrompts: [nodeBasePrompt]
        })
        return;
    }

    res.status(403).json({message: "You cant access this"})
    return;

})

app.post("/chat", async (req, res) => {
    const messages = req.body.messages;
    const {text} = await generateText({
        model : google("gemini-2.0-flash-exp") ,
        messages: messages,
        maxTokens: 8000,
        system: getSystemPrompt()
    })

    console.log(text);

    // res.json({
    //     response: (response.content[0] as TextBlock)?.text
    // });

    res.json({ response : text}); 
})

app.listen(3000);

