use std::io;

//if struct wants to use clone method
//all its elements must implement this method
#[derive(PartialEq, Clone)]
enum Token_type{
    Integer,
    Plus,
    Minus,
    Multi,
    Div,
    EoF,
    Empty
}

//we going to need a copy of instance later
#[derive(Clone)]
struct Token {
    token_type : Token_type,
    token_value : i64,
}

struct Interpreter {
    text : Vec<char>,
    position : usize,
    current_token : Token,
    current_char : char,
    input_end : bool,
}

impl Interpreter {
    fn new(input_text: String) -> Interpreter {

        //transfer input string into vector of chars
        let chars : Vec<char> = input_text.chars().collect();
        let c = chars[0];
        let empty_token = Token{ token_type: Token_type::Empty, token_value: 0};

        Interpreter {
            text: chars,
            position: 0, 
            current_token: empty_token, 
            current_char: c,
            input_end : false,
        }
    }

    fn error(&self) {
        panic!("Error parsing input");
    }

    fn advance(&mut self) {
        self.position += 1;
        let length = self.text.len(); 
    
        if self.position > length - 1 {
            self.input_end = true;
        }
        else {
            self.current_char = self.text[self.position];
        }
    }

    fn integer(&mut self) -> i64{
        let mut result = String::new();

        while !self.input_end && self.current_char.is_digit(10){
            result.push(self.current_char);
            self.advance();
        }
        
        let result: i64 = result.parse()
            .ok()
            .expect("not a number");

        result
    }

    fn get_next_token(&mut self) -> Token{
        
        while !self.input_end{
            
            if self.current_char.is_digit(10){
                return Token{token_type: Token_type::Integer,
                             token_value: self.integer()}
            }

            if self.current_char == '+'{
                self.advance();
                return Token{token_type: Token_type::Plus,
                             token_value: 1}
            }

            if self.current_char == '-' {
                self.advance();
                return Token{token_type: Token_type::Minus,
                             token_value: -1}
            }

            if self.current_char == '*'
            {
                self.advance();
                return Token{token_type: Token_type::Multi,
                             token_value: 2}
            }

            if self.current_char == '/'{
                self.advance();
                return Token{token_type: Token_type::Div,
                             token_value: -2}
            }

            self.error();
        }

        Token{token_type: Token_type::EoF, token_value: 0}
    }

    fn eat(&mut self, matched_type: Token_type){
        if self.current_token.token_type == matched_type{
            self.current_token = self.get_next_token();
        }
        else {
            self.error();
        }
    }

    fn expr(&mut self) -> i64{
        self.current_token = self.get_next_token();

        let left = self.current_token.clone(); //we need to make a copy of token before
        self.eat(Token_type::Integer); //rewriting

        
        let op = self.current_token.clone();
        
        match op.token_type {
            Token_type::Plus => self.eat(Token_type::Plus),
            Token_type::Minus => self.eat(Token_type::Minus),
            Token_type::Multi => self.eat(Token_type::Multi),
            Token_type::Div => self.eat(Token_type::Div),
            _ => self.error()
        }


        let right = self.current_token.clone();
        self.eat(Token_type::Integer);
        
        match op.token_type {
            Token_type::Plus => left.token_value + right.token_value,
            Token_type::Minus => left.token_value - right.token_value,
            Token_type::Multi => left.token_value * right.token_value,
            Token_type::Div => left.token_value / right.token_value,
            _ => panic!("this should not happen")
        }
    
    }
}

fn main() {

    loop {
        let mut input = String::new();
        
        io::stdin().read_line(&mut input)
            .ok()
            .expect("error");
        
        if input.len() > 1 { 
            input.pop(); //pop /n at the end of input  
        }
        else {
            continue; //skip empty input
        }

        let mut int = Interpreter::new(input); 
        let result = int.expr();

        println!(">> {}", result);
    }
}
