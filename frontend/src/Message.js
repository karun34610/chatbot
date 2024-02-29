import {Box,Typography} from "@mui/material";

export default function Message(props) {
  return (
    <div>
      <Box
        sx={{
          my: 2,
          display: "flex",
          flexFlow: "row",
          color:props.isCustomer ? "white" : "white",
          justifyContent: props.isCustomer ? "right" : "left",
          backgroundColor:props.isCustomer ? "#353441" : "#41404f" ,
          padding:1
        }}
      >
        <Box>
          <Typography gutterBottom variant="body2" component="div" sx={{mt: 1.5}}>
            {props.content}
            <br/>
            {props.accuracy ? <label style={{fontSize:"0.7rem"}}>90%</label> : <></>}
          </Typography>
          
        </Box>
      </Box>
    </div>
  );
}