(**
 * Substitute
 * Substitutes things for other things in files.
 *
 * Compiling:
 *  ocamlc -o substitute str.cma substitute.ml
 * Example usage:
 *  echo '$0 $1!' | ./substitute '$0->Hello' '$1->world'
 *  #=> Hello world!
 * Potential issues:
 *  May substitute more than you'd like, so keep a 
 *  backup.
 * Parameters:
 *  Each parameter is in the form of a placeholder,
 *  the delimiter '->' and a substitution
 *  (best to look at the example).
 * Requires:
 *  Ocaml (http://caml.inria.fr/)
 * Author:
 *  Konrad Siek
 *)

(**
 * Delimiter for program arguments.
 * Establishes which part of the argument is the 
 * placeholder and which is the substitution.
 *)
let delimiter = "->";;
(**
 * Substitutes a placeholder with a phrase.
 * This function runs recursivelly on a list.
 * @param what - placeholder
 * @param into - substitution
 * @param contents - array of strings to traverse
 * @return an array of strings
 *)
let substitute functions contents =
    let rec apply functions content =
        match functions with
        | transform::tail -> 
            apply tail (transform content)
        | [] -> content
    in
    let result = ref [] in
    let iterate element =
        result := !result @ 
        [apply functions element]
    in
    List.iter iterate contents;
    !result
;;
(**
 * Outputs the contents of an array to standard
 * output.
 * @param contents - an array of strings
 *)
let rec print_contents contents = 
    match contents with
    | head::tail -> 
        print_endline head; 
        print_contents tail
    | [] -> () 
;;
(**
 * Converts a program argument into a translation
 * function.
 * @param argument
 * @return a function
 *)
let handle_argument argument = 
    let regex = Str.regexp_string delimiter in
    let bits = Str.split regex argument in 
    if List.length bits < 2 then (
        prerr_string 
            ("Illegal argument: '" ^ argument ^ "'");
        prerr_newline ();
        fun input -> input
    ) else (
        let from = Str.regexp_string (List.hd bits) in 
        let into = List.fold_left
            (fun a b -> a ^ delimiter ^ b) 
            (List.hd (List.tl bits)) 
            (List.tl (List.tl bits)) in
        fun input -> 
            (Str.global_replace from into input)
    )
;;
(**
 * Converts a list of program arguments into a
 * list of translation functions.
 * @param arguments
 * @return functions
 *)
let handle_arguments arguments = 
    let rec handle_arguments arguments results = 
        match arguments with
        | head::tail -> 
            let argument = 
                (handle_argument head) in 
            handle_arguments tail
                (results @ [argument])
        | [] -> results
    in
    handle_arguments arguments []
;;
(**
 * Grab input from standard input - read until
 * an end of stream occurs.
 * @param unit
 * @return list of strings
 *)
let read_input () =
    let list = ref [] in 
    let _ = try 
        while true do
            let line = input_line stdin in
            list := !list @ [line]
        done
    with _ -> () in 
    !list
;;    

(* Convert argument vector to list *)
let arguments = (List.tl (Array.to_list Sys.argv)) in
(* Translate arguments to functions *)
let functions = handle_arguments arguments in
(* Read contents from standard input *)
let contents = read_input () in 
(* Apply transformations on contents *)
let results = substitute functions contents in
(* And print results to standard output *)
print_contents results;;
