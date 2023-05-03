extern crate noise;
extern crate config;

use crate::noise::Seedable;
use noise::{NoiseFn, Perlin};
use std::error::Error;
use std::fs::{create_dir_all, File};
use std::io::prelude::*;
use config::{Config, File as CFile};
use std::env;

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args.len() > 4 {
        panic!("Invalid number of arguments. Usage: `cargo run new` or `cargo run <chunk_x> <chunk_y>`");
    }

    let mut settings = Config::default();
    settings.merge(CFile::with_name("config.toml"))?;

    let map_size = settings.get::<usize>("map_size")?;
    let seed = settings.get::<u32>("seed")?;
    let chunk_width = settings.get::<usize>("chunk_width")?;
    let chunk_height = settings.get::<usize>("chunk_height")?;
    let save_path = settings.get::<String>("save_path")?;
    let frequency = settings.get::<f64>("frequency")?;
    let lacunarity = settings.get::<f64>("lacunarity")?;
    let persistence = settings.get::<f64>("persistence")?;
    let octaves = settings.get::<usize>("octaves")?;
    let chunks_to_generate = settings.get::<usize>("chunks_to_generate")?;

    create_dir_all(&save_path)?;

    let perlin = Perlin::new().set_seed(seed);

    if args[1] == "new" {
        generate_swirl_chunks(chunks_to_generate, &settings)?;
    } else {
        let chunk_x: isize = args[1].parse()?;
        let chunk_y: isize = args[2].parse()?;
        generate_chunk(chunk_x, chunk_y, &settings)?;
    }

    Ok(())
}

fn generate_swirl_chunks(chunks_to_generate: usize, settings: &Config) -> Result<(), Box<dyn Error>> {
    let mut x = 0;
    let mut y = 0;
    let mut dx = 0;
    let mut dy = -1;

    for _ in 0..(chunks_to_generate + 1) {
        if x == y || (x < 0 && x == -y) || (x > 0 && x == 1 - y) {
            let temp = dx;
            dx = -dy;
            dy = temp;
        }

        if x != 0 || y != 0 {
            generate_chunk(x, y, settings)?;
        }

        x += dx;
        y += dy;
    }

    Ok(())
}

fn write_dummy_texture_coordinates(file: &mut File, chunk_width: usize, chunk_height: usize) -> Result<(), Box<dyn Error>> {
    for _j in 0..chunk_height {
        for _i in 0..chunk_width {
            writeln!(file, "vt 0.0 0.0")?;
        }
    }
    Ok(())
}

fn generate_chunk(chunk_x: isize, chunk_y: isize, settings: &Config) -> Result<(), Box<dyn Error>> {
    let map_size = settings.get::<usize>("map_size")?;
    let seed = settings.get::<u32>("seed")?;
    let chunk_width = settings.get::<usize>("chunk_width")?;
    let chunk_height = settings.get::<usize>("chunk_height")?;
    let save_path = settings.get::<String>("save_path")?;
    let frequency = settings.get::<f64>("frequency")?;
    let lacunarity = settings.get::<f64>("lacunarity")?;
    let persistence = settings.get::<f64>("persistence")?;
    let octaves = settings.get::<usize>("octaves")?;
    let perlin = Perlin::new().set_seed(seed);

    let mut chunk_data = vec![vec![0.0; chunk_width]; chunk_height];

    for j in 0..chunk_height {
        for i in 0..chunk_width {
            let mut noise_value = 0.0;
            let mut world_x = (chunk_x as f64 * chunk_width as f64 + i as f64) * frequency;
            let mut world_y = (chunk_y as f64 * chunk_height as f64 + j as f64) * frequency;

            let mut amplitude = 1.0;

            for _ in 0..octaves {
                noise_value += perlin.get([world_x, world_y]) * amplitude;
                world_x *= lacunarity;
                world_y *= lacunarity;
                amplitude *= persistence;
            }

            let height = (noise_value + 1.0) / 2.0;
            chunk_data[j][i] = height;
        }
    }

    let file_path = format!("{}/chunk_{}_{}.obj", save_path, chunk_x, chunk_y);
    let mut file = File::create(file_path)?;

        // Write vertices
    for j in 0..chunk_height {
        for i in 0..chunk_width {
            writeln!(
                file,
                "v {} {} {}",
                i as f32,
                chunk_data[j][i] as f32,
                j as f32
            )?;
        }
    }
    // Write dummy texture coordinates
    write_dummy_texture_coordinates(&mut file, chunk_width, chunk_height)?;

    // Write faces with normals
    for j in 0..chunk_height - 1 {
        for i in 0..chunk_width - 1 {
            // First loop of faces
            let v1 = (j * chunk_width + i) as u32;
            let v2 = (j * chunk_width + i + 1) as u32;
            let v3 = ((j + 1) * chunk_width + i) as u32;

            let normal = calculate_normal(
                (i as f32, -chunk_data[j][i] as f32, j as f32),
                ((i + 1) as f32, -chunk_data[j][i + 1] as f32, j as f32),
                (i as f32, -chunk_data[j + 1][i] as f32, (j + 1) as f32),
            );

            writeln!(file, "vn {} {} {}", normal.0, -normal.1, normal.2)?;
            writeln!(
                file,
                "f {}/{}/1 {}/{}/1 {}/{}/1",
                v3 + 1,
                v3 + 1,
                v2 + 1,
                v2 + 1,
                v1 + 1,
                v1 + 1
            )?;

            // Second loop of faces
            let v1 = (j * chunk_width + i + 1) as u32;
            let v2 = ((j + 1) * chunk_width + i + 1) as u32;
            let v3 = ((j + 1) * chunk_width + i) as u32;

            let normal = calculate_normal(
                ((i + 1) as f32, -chunk_data[j][i + 1] as f32, j as f32),
                ((i + 1) as f32, -chunk_data[j + 1][i + 1] as f32, (j + 1) as f32),
                (i as f32, -chunk_data[j + 1][i] as f32, (j + 1) as f32),
            );

            writeln!(file, "vn {} {} {}", normal.0, -normal.1, normal.2)?;
            writeln!(
                file,
                "f {}/{}/1 {}/{}/1 {}/{}/1",
                v3 + 1,
                v3 + 1,
                v2 + 1,
                v2 + 1,
                v1 + 1,
                v1 + 1
            )?;
        }
    }

fn calculate_normal(v1: (f32, f32, f32), v2: (f32, f32, f32), v3: (f32, f32, f32)) -> (f32, f32, f32) {
    let vec1 = (v2.0 - v1.0, v2.1 - v1.1, v2.2 - v1.2);
    let vec2 = (v3.0 - v1.0, v3.1 - v1.1, v3.2 - v1.2);
    let normal = (
        vec1.1 * vec2.2 - vec1.2 * vec2.1,
        vec1.2 * vec2.0 - vec1.0 * vec2.2,
        vec1.0 * vec2.1 - vec1.1 * vec2.0,
    );
    let length = (normal.0 * normal.0 + normal.1 * normal.1 + normal.2 * normal.2).sqrt();
    (normal.0 / length, normal.1 / length, normal.2 / length)
}

    Ok(())
}
