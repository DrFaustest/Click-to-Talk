# Talk-to-Click: Voice Controlled Internet Navigation

## Overview
**Talk-to-Click** is a proposed Chrome extension that enables voice-controlled mouse navigation for web browsing.  
This adaptive technology is designed to support individuals with fine-motor and dexterity challenges—such as those affected by Parkinson’s disease or declining motor coordination—who struggle with traditional mouse or trackpad use.  

By translating voice input into precise mouse movements and clicks, the extension reduces both the **gulf of execution** and the **gulf of evaluation**, enabling users to navigate the internet more effectively and independently.

---

## Motivation
Operating a mouse requires multiple fine-motor skills:  
- Pinpointing a location on the screen.  
- Holding the cursor steady.  
- Executing the correct click (left vs. right).  

For many users with motor coordination difficulties, these actions may fail at the execution phase. Mis-clicks often go unnoticed, leading to unintended outcomes and user frustration.  

**Talk-to-Click** aims to bridge this accessibility gap by replacing complex motor actions with **intuitive voice commands**.

---

## Technology
The implementation will rely on existing, widely available hardware and software:  

- **Input Device:** Computer’s built-in microphone (standard on most laptops, monitors, and mobile devices).  
- **Voice Recognition:** Python speech-to-text libraries to process and interpret spoken commands.  
- **Action Mapping:** Speech input translated into text commands that trigger mouse movements or clicks.  

---

## Features (Planned & Potential)
**Initial Features:**  
- Mouse navigation via commands: `"up"`, `"down"`, `"left"`, `"right"`.  
- Mouse click commands: `"left click"`, `"right click"`.  
- Browser navigation: `"back"`, `"forward"`, `"reload"`.  
- Address bar control via voice commands.  

**Future Features:**  
- Command `"find"` to visually emphasize the cursor with a highlight or circle.  
- More natural language processing for advanced voice interaction.  
- Potential for **full mouse functionality** controlled entirely through speech.  

---

## Team Organization

- **Megan Backman** – Documentation Team Lead  
  *Project management, creativity, and documentation leadership.*  

- **Allison Coates** – Documentation Team  
  *Problem-solving, organization, detail-oriented, Python experience.*  

- **Scott Faust** – Implementation & Video Team Lead  
  *Software engineering, problem solving, technical writing, and communication of complex concepts.*  

- **Luke Mabie** – Implementation Team  
  *End-to-end software development, collaboration, and customer-focused coding.*  

- **Alexander Jimenez** – Implementation Team Lead  
  *Programming, design innovation, and team coordination.*  

- **Hunter Pope** – Implementation Team  
  *Back-end programming and graphic design expertise.*  

---

## Roadmap
1. **Phase 1 – Prototype**  
   - Voice-to-text mapping for simple directional and click commands.  
   - Basic integration with Chrome for mouse control.  

2. **Phase 2 – Browser Control**  
   - Navigation commands (back, reload, forward).  
   - Address bar activation.  

3. **Phase 3 – Enhanced Accessibility**  
   - Highlight/circle cursor with `"find"` command.  
   - Expanded natural language interaction.  

4. **Phase 4 – Full Mouse Replacement**  
   - Comprehensive voice-controlled functionality.  
   - Potential integration with accessibility APIs and third-party tools.  

---

## License
TBD (to be decided by the team).  

---

## Acknowledgments
This project is inspired by the need for **inclusive, accessible technology** that empowers individuals with motor coordination challenges to navigate the web confidently and independently.
