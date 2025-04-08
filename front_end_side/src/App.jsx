//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import './App.css'
import {useState} from "react"

import ClearText from "./assets/cross.svg?react"
import ClearTextAttendedState from "./assets/cross_attended.svg?react"
import LoadedDoc from "./assets/loaded_doc.svg?react"

import {FileUploader} from "react-drag-drop-files";

var blockRows = 10
var blockCols = 40
var inputTextMaxLength = 3000
var inputFileMaxSize = 5 // Megabytes

const approvedFileTypes = ["TXT", "PDF", "DOC", "DOCX"]

function LogoBar() {

}

function ClearTextButton({ id, setText }) {
  const [attention, setAttention] = useState(false)
  
  function handleClick() {
    document.getElementById(id).value = "";
    setText({ value: "" });
  }
  
  function handleMouseEnter() {
    setAttention(true);
  }
  
  function handleMouseLeave() {
    setAttention(false);
  }
  
  let buttonImage;
  
  if (!attention) {
    buttonImage = <ClearText></ClearText>
  } else {
    buttonImage = <ClearTextAttendedState></ClearTextAttendedState>
  }
  
  return (
    <>
      <button onClick={handleClick} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}
              style={{background : 'transparent', border: 'none', outline: 'none'}}>
        {buttonImage}
      </button>
    </>
  )
}

function OverflowCounter({ count, bound, inputFromTextFlag}) {
  let um;
  
  if (inputFromTextFlag) {
    um = 'symbols';
  } else {
    um = 'MB';
  }
  
  return (
    <label htmlFor="user_text"> {count} / {bound} {um} </label>
  )
}

function InputFromTextWindow({ text, setText }) {
  function handleTextChanges(event) {
    setText({value : event.target.value})
    //console.log(text.value)
  }
  
  return (
    <>
      <textarea rows={blockRows} cols={blockCols}
                placeholder="Enter some text here..." maxLength={inputTextMaxLength}
                onChange={handleTextChanges} id="user_text"></textarea>
      <ClearTextButton id="user_text" setText={setText}></ClearTextButton>
    </>
  )
}

function InputFromFileWindow({ file, setFile }) {
  function onFileDropped(file) {
    setFile(file);
    console.log(file);
  }
  
  let div_text;
  
  if (file === null) {
    div_text = 'Drop [.txt, .pdf, .doc(x)] files here or click ot select it'
  } else {
    div_text =
      <>
        <div className="loaded_icon">
          <LoadedDoc></LoadedDoc>
        </div>
        <div className="text_near_loaded_file_icon">
          Loaded [{file.name.split('.').pop()}] file
        </div>
        <div className="text_under_loaded_file_icon">
          {file.name}
        </div>
      </>
  }
  
  return (
    <>
      <FileUploader
        children={
          <div className="file_input">
            <div className="file_input_info">
              {div_text}
            </div>
          </div>
        }
        
        types={approvedFileTypes}
        handleChange={onFileDropped}
        name="input"
        maxSize={inputFileMaxSize}
        
        dropMessageStyle={{
          height: '392px', width: '757px', position: 'absolute', left: '-382px'}}>
      </FileUploader>
    </>
  )
}

function TextInputButton({ inputFromTextFlag, setInputFromTextFlag, setText}) {
  function handleClick() {
    if (!inputFromTextFlag) {
      //console.log('changed!')
      setInputFromTextFlag(true);
      setText("");
    }
  }
  
  return (
    <button onClick={handleClick}>Text</button>
  )
}

function FileInputButton({ inputFromTextFlag, setInputFromTextFlag, setFile }) {
  function handleClick() {
    if (inputFromTextFlag) {
      setInputFromTextFlag(false)
      setFile(null);
    }
  }
  
  return (
    <button onClick={handleClick}>File</button>
  )
}

function InputEnvironment() {
  const [inputFromTextFlag, setInputFromTextFlag] = useState(true);
  const [userText, setUserText] = useState("");
  const [userFile, setFile] = useState(null);
  
  let displayedBlock, maxSize, currentSize;
  
  if (inputFromTextFlag) {
    displayedBlock = <InputFromTextWindow text={userText} setText={setUserText}></InputFromTextWindow>
    maxSize = inputTextMaxLength
    currentSize = (userText.value !== undefined) ? (userText.value.length) : (0) + "";
  } else {
    displayedBlock = <InputFromFileWindow setFile={setFile} file={userFile}></InputFromFileWindow>
    maxSize = inputFileMaxSize
    currentSize = (userFile !== null) ? ((userFile.size / (1048576)).toFixed(5)) : (0) + "";
  }
  
  return (
    <>
      <div className="left_block">
        <div className="buttons">
          <div className="text_button">
            <TextInputButton inputFromTextFlag={inputFromTextFlag}
                             setInputFromTextFlag={setInputFromTextFlag} setText={setUserText}></TextInputButton>
          </div>
          <div className="file_button">
            <FileInputButton inputFromTextFlag={inputFromTextFlag}
                             setInputFromTextFlag={setInputFromTextFlag} setFile={setFile}></FileInputButton>
          </div>
          <div className="overflow_counter">
            <OverflowCounter count={currentSize} bound={maxSize} inputFromTextFlag={inputFromTextFlag}></OverflowCounter>
          </div>
          <SendButton></SendButton>
        </div>
        
        <div className="input_window">
          {displayedBlock}
        </div>
      </div>
      
    </>
  )
}

function ResponseWindow() {
  return (
    <>
      <div className="right_block">
        <div className="right_block_label">
          <label> Analysis: </label>
        </div>
        <div>
          <textarea rows={blockRows} cols={blockCols} readOnly
                    placeholder="There would be result of analysis"></textarea>
        </div>
      </div>
    </>
  )
}

function SendButton() {
 return (
   <>
     <div className="send_button">
       <button> Analyze </button>
     </div>
   </>
 )
}

function WorkArea() {
  return (
    <>
      <InputEnvironment></InputEnvironment>
      <ResponseWindow></ResponseWindow>
    </>
  )
}

function App() {
  return (
    <div>
      <WorkArea></WorkArea>
    </div>
  )
}

export default App
