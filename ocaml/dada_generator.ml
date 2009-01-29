(**
 * Dada generator
 * Generates a completely useless but aesthetically pleasing dada program
 * 
 * Potential issues:
 *  None
 * Parameters:
 *  number of internal functions
 *  name of the dadaistic function
 *  list of passed parameters
 * Requires:
 *  Ocaml (http://caml.inria.fr/)
 *  Sense of humor
 *)

(**
 * Function responsible for generating dadaistic programs basing on the 
 * supplied parameters
 * @param function_name the name of the main function
 * @param parameter_list a list of strings which will be inserted as the 
 *  body of the inner-most function
 * @param nested_function_count the number of functions generated inside 
 *  the main function
 * @author Konrad Siek
 *)
let generate_dada function_name parameter_list nested_function_count =
   let rec list_to_string list =
      match list with 
        | head::tail -> head ^ " " ^ (list_to_string tail)
        | [] -> ""
   in
   let rec tabs count = 
      if count = 0 then
         ""
      else
         "   " ^ (tabs (count - 1))
   in
   let program = ref ("let " ^ function_name  ^ " " ^ 
        (list_to_string parameter_list) ^ "=\n") in
   let _ = for i = 1 to nested_function_count do
     program := !program ^ (tabs i);
     program := !program ^ "let " ^ function_name ^ " " ^ 
        (list_to_string parameter_list) ^ "=\n"
   done in
   program := !program ^ (tabs (nested_function_count + 1)) ^ 
        (list_to_string parameter_list) ^ "\n";
   let _ = for i = nested_function_count downto 1 do
     program := !program ^ (tabs i);
     program := !program ^ "in " ^  function_name ^ " " ^ 
        (list_to_string parameter_list) ^ "\n"
   done in
   program := !program ^ ";;\n";
   !program
;;

(* Main method calling the generation function. *)
if Array.length Sys.argv > 3 then 
   let count = int_of_string Sys.argv.(1) in
   let function_name = Sys.argv.(2) in
   let parameters = Array.to_list 
    (Array.sub Sys.argv 3 (Array.length Sys.argv - 3)) in
   let program = generate_dada function_name parameters count in
   print_endline program
else
   print_endline ("Usage:\n\t" ^ Sys.argv.(0) ^ " <function_count> " ^ 
        "<main_function_name> <parameter> [ ... <parameter> ]")
;;
