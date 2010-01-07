(**
 * Youtube-ML
 *
 * Use youtube-dl to download videos from a list saved in a file. 
 * Sort of batch-process youtube-dl downloads.
 *
 * Compiling:
 *  ocamlc -o youtube-ml str.cma youtube.ml
 *
 * Example usage:
 *  Download using a file in best quality:
 *      ./youtube-ml --best-quality list_of_files.txt
 *  Download using a bash ad-hoc file and in quiet mode:
 *  ./youtube-ml --quiet <<$
 *      some_filename.flv --- http://some_address/gibberish
 *      other_filename.flv --- http://other_address/gibberish
 *  $
 *
 * Parameters:
 *  --help - show usage information,
 *  --quiet - do not display additional information messages,
 *  --best-quality - download in MP4 instead of FLV format.
 *
 * Requires:
 *  youtube-dl (http://bitbucket.org/rg3/youtube-dl/wiki/Home)
 *
 * Author:
 *  Konrad Siek
 *
 * License:
 * 	Copyright 2010 Konrad Siek 
 *
 * 	This program is free software: you can redistribute it and/or modify
 * 	it under the terms of the GNU General Public License as published by
 * 	the Free Software Foundation, either version 3 of the License, or
 * 	(at your option) any later version.
 *
 * 	This program is distributed in the hope that it will be useful,
 * 	but WITHOUT ANY WARRANTY; without even the implied warranty of
 * 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * 	GNU General Public License for more details.
 *
 * 	You should have received a copy of the GNU General Public License
 * 	along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *)
open Str;;

let youtube_cmd = "youtube-dl";;
let delimiter = "[\t ]+---[\t ]+";;
let best_quality_flag = ref false;;
let quiet_flag = ref false;;

exception InvalidString of string ;;

type filename = string;;
type address = string;;
type clip = filename * address;;

(* Convert line into a tupple of type clip. *)
let clip_of_string line = 
    let regex = Str.regexp delimiter in
    let result = Str.split regex line in
    match result with
    | file :: http :: [] -> (file, http) 
    | _ -> raise (InvalidString ("Line '" ^ line ^ "' is invalid."))
;;

(* Read a file and break it down into tupples. *)
let read_file filename =     
    let channel = open_in filename in
    let rec read channel result = 
    try 
        let line = input_line channel  in
        let clip = clip_of_string line in
        let result = result @ [clip] in
        read channel result
(* with Invalid_string -> raise Invalid_string *)
    with 
        | InvalidString message -> raise (InvalidString message)
        | _ -> result
    in
    read channel []           
;;

(* Print completed message. *)
let print_completed output =
    if not !quiet_flag then 
        print_endline ("Download into file '" ^ output ^ "' completed.")
;;

(* Print incomplete message. *)
let print_incomplete output =
    if not !quiet_flag then 
        print_endline ("Download into file '" ^ output ^ "' problematic.")
;;

(* Print that a file is being downloaded. *)
let print_intro http output =
    if not !quiet_flag then 
        print_endline ("Downloading " ^ http ^ " as " ^ output)
;;

(* Download clips listed in one file. *)
let download filename = 
    let clips = read_file filename in    
    let download (output, http) = 
        let command = if !best_quality_flag then
            youtube_cmd ^ " -b -o \"" ^ output ^ "\" -q \"" ^ http ^ "\""
        else 
            youtube_cmd ^ " -o \"" ^ output ^ "\" -q \"" ^ http ^ "\"" in
        print_intro http output;
        let result = Sys.command command in
        if result = 0 then
            print_completed output
        else 
            print_incomplete output
    in
    List.iter download clips        
;;

(* Print message on how to use the program.  *)
let print_usage program_name =
    let usage = 
      "Usage: \n" ^
      "\t" ^ program_name ^ " " ^ "filename [filename ...] \n" ^
      "\t" ^ program_name ^ " " ^ "--best-quality filename [filename ...] \n" ^
      "\t" ^ program_name ^ " " ^ "--help \n" ^
      "Files: \n" ^
      "\t" ^ "The files should consist of lines, each line composed of:" ^
      "\t\t" ^ " - the file to which save the song," ^
      "\t\t" ^ " - the delimiter consisting of three hyphens ('---')" ^
      "\t\t" ^ "   which can be surrounded by tabs and spaces," ^
      "\t\t" ^ " - address of the song."
    in
    print_endline usage
;;
    
(* Print message that given file does not exist. *)
let print_file_not_exists file =
    let message = "File '" ^ file ^ "' does not exist. " in
    print_endline message
;;

(* Process all arguments and conduct appropriate action. *)
let rec process_args program args =
    match args with
    | arg :: tail -> 
        if String.length arg > 1 && String.get arg 0 = '-' then
            match arg with
            | "--help" -> print_usage program
            | "--best-quality" ->
                best_quality_flag := true;
                process_args program tail
            | "--quiet" ->
                quiet_flag := true;
                process_args program tail
            | _ -> print_usage program
        else
            download arg
    | [] -> ()
;;
    
(* Read command-line arguments and launch operations. *)
let main () = 
let length = Array.length Sys.argv in 
let program = Sys.argv.(0) in
    if length > 1 then
        process_args program (List.tl (Array.to_list Sys.argv))
    else 
        print_usage program
;;       

main ()           
