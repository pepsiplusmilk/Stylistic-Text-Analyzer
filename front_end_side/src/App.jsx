//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import './App.css'
import {useState} from "react";
import {useRef} from "react";
//import {ClearText} from "./assets/cross.svg"

var blockRows = 10
var blockCols = 40
var inputTextMaxLength = 3000

function LogoBar() {

}

function ClearTextButton() {
  return (
    <>
      <button></button>
    </>
  )
}

function InputFromTextWindow() {
  const [state, setState] = useState("");
  
  function handleTextChanges(event) {
    setState({value : event.target.value})
    console.log(state.value())
  }
  
  return (
    <>
      <textarea rows={blockRows} cols={blockCols}
                 placeholder="Enter some text here..." maxLength={inputTextMaxLength}
                onChange={handleTextChanges}></textarea>
      <ClearTextButton></ClearTextButton>
    </>
   
  )
}

function InputFromFileWindow() {
  return (
    <textarea rows={blockRows} cols={blockCols} readOnly></textarea>
  )
}

function TextInputButton({ inputFromTextFlag, setInputFromTextFlag }) {
  function handleClick() {
    if (!inputFromTextFlag) {
      console.log('changed!')
      setInputFromTextFlag(true)
    }
  }
  
  return (
    <button onClick={handleClick}>Text</button>
  )
}

function FileInputButton({ inputFromTextFlag, setInputFromTextFlag }) {
  function handleClick() {
    if (inputFromTextFlag) {
      setInputFromTextFlag(false)
    }
  }
  
  return (
    <button onClick={handleClick}>File</button>
  )
}

function InputEnvironment() {
  const [inputFromTextFlag, setInputFromTextFlag] = useState(true)
  
  let displayedBlock;
  
  if (inputFromTextFlag) {
    displayedBlock = <InputFromTextWindow></InputFromTextWindow>
  } else {
    displayedBlock = <InputFromFileWindow></InputFromFileWindow>
  }
  
  return (
    <>
      <div className="left_block">
        <div className="buttons">
          <div className="text_button">
            <TextInputButton inputFromTextFlag={inputFromTextFlag}
                             setInputFromTextFlag={setInputFromTextFlag}></TextInputButton>
          </div>
          <div className="file_button">
            <FileInputButton inputFromTextFlag={inputFromTextFlag}
                             setInputFromTextFlag={setInputFromTextFlag}></FileInputButton>
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
